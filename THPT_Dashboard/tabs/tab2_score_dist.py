import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# CẤU HÌNH & MAPPING
# ==========================================
SUBJECT_MAP = {
    'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
    'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
    'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
}

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ (CHART COMPONENTS)
# ==========================================
def plot_histogram(df_year, subject_col):
    """Vẽ Histogram phân phối điểm cho 1 năm cụ thể"""
    data = df_year[df_year[subject_col].notna()]
    
    # Trả về biểu đồ trống nếu không có dữ liệu
    if data.empty:
        return go.Figure().update_layout(title="Không có dữ liệu cho năm này")

    fig = px.histogram(
        data, x=subject_col, 
        nbins=40, # Chia khoảng 0.25 điểm
        color_discrete_sequence=['#14357A'], # Màu Super Store
        opacity=0.8
    )
    
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Điểm số", dtick=1, range=[-0.5, 10.5], showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(title="Số lượng thí sinh", showgrid=True, gridcolor='#f0f0f0')
    )
    return fig

def plot_score_brackets(df_full, subject_col):
    """Biểu đồ Cột chồng theo Phân khúc điểm (Không Lag, Dễ đọc nhất)"""
    data = df_full[df_full[subject_col].notna() & df_full['nam'].notna()].copy()
    if data.empty: return go.Figure()

    # Tạo phân khúc (Bins)
    bins = [-1, 4.99, 6.99, 7.99, 10]
    labels = ['Dưới 5', '5 - 7', '7 - 8', 'Từ 8 - 10']
    
    # Phân loại điểm vào các nhóm
    data['Phân khúc'] = pd.cut(data[subject_col], bins=bins, labels=labels)
    
    # Tính toán tỷ lệ % cho từng năm (Siêu tốc độ)
    grouped = data.groupby(['nam', 'Phân khúc'], observed=True).size().reset_index(name='Số lượng')
    grouped['Tỷ lệ %'] = grouped.groupby('nam')['Số lượng'].transform(lambda x: x / x.sum() * 100)
    grouped['nam'] = grouped['nam'].astype(int).astype(str)

    fig = px.bar(
        grouped, x='nam', y='Tỷ lệ %', color='Phân khúc',
        text=grouped['Tỷ lệ %'].apply(lambda x: f"{x:.1f}%"),
        color_discrete_map={
            'Từ 8 - 10': '#2ca02c', # Xanh lá
            '7 - 8': '#1f77b4',     # Xanh dương
            '5 - 7': '#ff7f0e',     # Cam
            'Dưới 5': '#d62728'     # Đỏ
        }
    )
    
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', 
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Năm thi", showgrid=False),
        yaxis=dict(title="Tỷ lệ % Thí sinh", range=[0, 100], showgrid=False, visible=False), # Ẩn trục Y cho gọn
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title="")
    )
    return fig

# ==========================================
# MAIN RENDER FUNCTION
# ==========================================
def render(df):
    # --------------------------------------
    # 1. CSS STYLING (SUPER TỐI ƯU KHÔNG GIAN)
    # --------------------------------------
    st.markdown("""
        <style>
        /* Ép Streamlit giảm khoảng trống gốc */
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
        
        /* Header gọn gàng */
        .dash-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; }
        .dash-title { margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 1px;}
        .dash-subtitle { margin: 0; font-size: 13px; color: #A0AEC0;}
        
        /* Banner & Chart ép sát */
        .chart-banner { background-color: #14357A; color: white; padding: 5px 15px; font-size: 13px; font-weight: 600; border-radius: 4px 4px 0 0; margin-bottom: 0px; }
        .chart-container { background-color: white; padding: 10px; border-radius: 0 0 4px 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 10px; }
        
        /* KPI Cards ép sát */
        [data-testid="stMetric"] { background-color: white; border-top: 4px solid #051039; padding: 10px 15px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        [data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 700; color: #14357A; }
        </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 2. HEADER
    # --------------------------------------
    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">📈 SCORE DISTRIBUTION</h1>
            <p class="dash-subtitle">Phân tích phân hóa & Chất lượng đề thi theo từng môn học</p>
        </div>
    """, unsafe_allow_html=True)

# --------------------------------------
# 3. FILTER BAR
# --------------------------------------

    st.markdown("<div style='font-size: 15px; font-weight: bold; margin-bottom: 2px; color: #14357A;'>🎛️ Bộ lọc Phân tích</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1.5], gap="small")
    
    with f_col1:
        # Xử lý năm: Lọc bỏ NaN, ép về int
        years = sorted([int(y) for y in df['nam'].dropna().unique()], reverse=True)
        selected_year = st.selectbox("📅 Chọn Năm thi", years)
        
    with f_col2:
        selected_subject_name = st.selectbox("🎯 Chọn Môn học", list(SUBJECT_MAP.values()))
        subject_col = [k for k, v in SUBJECT_MAP.items() if v == selected_subject_name][0]
    
    with f_col3:
        # Tự tạo hộp thông báo mỏng nhẹ. 
        # margin-top: 28px giúp nó tụt xuống đúng bằng độ cao của dòng chữ "Chọn Năm thi" ở 2 cột trước
        st.markdown(f"""
            <div style="background-color: #F0F8FF; color: #051039; padding: 0px 15px; border-radius: 4px; font-size: 13.5px; margin-top: 28px; border: 1px solid #BEE3F8; border-left: 4px solid #14357A; display: flex; align-items: center; height: 39px;">
                <span>Đang xem: <b>{selected_subject_name}</b> &nbsp;|&nbsp; Histogram: <b>{selected_year}</b> &nbsp;|&nbsp; Cột chồng: Toàn giai đoạn</span>
            </div>
        """, unsafe_allow_html=True)

    # Tách dữ liệu an toàn
    df_year = df[df['nam'] == selected_year]
    subject_data_year = df_year[df_year[subject_col].notna()][subject_col]

    st.markdown("<div style='margin-bottom: -25px;'></div>", unsafe_allow_html=True) # Spacer rất mỏng thay cho st.divider()

    # --------------------------------------
    # 4. KPI CARDS (Dùng gap="small" ép sát)
    # --------------------------------------
    if not subject_data_year.empty:
        total_students = len(subject_data_year)
        avg_score = subject_data_year.mean()
        med_score = subject_data_year.median()
        pass_rate = (len(subject_data_year[subject_data_year >= 5]) / total_students) * 100

        k1, k2, k3, k4 = st.columns(4, gap="small")
        k1.metric("Tổng thí sinh thi", f"{total_students:,}")
        k2.metric("Điểm Trung bình", f"{avg_score:.2f}")
        k3.metric("Điểm Trung vị (Median)", f"{med_score:.2f}")
        k4.metric("Tỷ lệ điểm ≥ 5", f"{pass_rate:.1f}%")
    else:
        st.warning(f"⚠️ Không có dữ liệu thí sinh dự thi môn {selected_subject_name} trong năm {selected_year}.")

    # Đã xóa dòng <br> thừa ở đây để kéo chart lên sát KPI

    # --------------------------------------
    # 5. CHART GRID (Dùng gap="small" ép sát)
    # --------------------------------------
    col_left, col_right = st.columns([1, 1.2], gap="small")

    with col_left:
        st.markdown(f'<div class="chart-banner">1. Phổ điểm chi tiết môn {selected_subject_name} ({selected_year})</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_histogram(df_year, subject_col), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown(f'<div class="chart-banner">2. Cơ cấu điểm môn {selected_subject_name} (Các năm)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_score_brackets(df, subject_col), use_container_width=True) 
        st.markdown('</div>', unsafe_allow_html=True)