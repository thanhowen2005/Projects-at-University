import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc

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
        height=380,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Điểm số", dtick=1, range=[-0.5, 10.5], showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(title="Số lượng thí sinh", showgrid=True, gridcolor='#f0f0f0')
    )
    return fig

def plot_subject_boxplot(df_year, subject_col, selected_year):
    """Biểu đồ Boxplot: Soi chi tiết dải điểm và điểm ngoại lệ (Outliers)"""
    data = df_year[df_year[subject_col].notna()].copy()
    if data.empty: return go.Figure()
    
    data['nam'] = str(selected_year)
    
    fig = px.box(
        data, x='nam', y=subject_col,
        color_discrete_sequence=['#FF7F0E'], 
        points='outliers' 
    )
    
    fig.update_layout(
        height=380,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Năm", showgrid=False), 
        yaxis=dict(title="Dải điểm", dtick=1, range=[-0.5, 10.5], showgrid=True, gridcolor='#f0f0f0')
    )
    return fig


def plot_score_line_trend(df_full, subject_col, selected_year):
    """Biểu đồ đường: So sánh phổ điểm năm nay với bóng ma lịch sử (Đa màu sắc)"""
    # Tính toán số lượng thí sinh theo từng mức điểm và năm
    trend_data = df_full[df_full[subject_col].notna()].groupby(['nam', subject_col]).size().reset_index(name='count')
    
    fig = go.Figure()
    years = sorted(trend_data['nam'].unique())
    
    # Tạo danh sách màu cho các lines
    colors = ['#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    for i, year in enumerate(years):
        df_year = trend_data[trend_data['nam'] == year]
        is_current = (year == selected_year)
        
        # Lấy màu tương ứng cho năm này (cố định màu theo thứ tự năm)
        year_color = colors[i % len(colors)]
        
        # Style: độ đậm/nhạt và kiểu nét (liền/đứt)
        line_style = dict(color=year_color, width=4) if is_current else dict(color=year_color, width=1.5, dash='dot')
        opacity = 1.0 if is_current else 0.7
        
        # icon cho năm đang chọn ở Legend
        name_label = f"🔥 Năm {int(year)}" if is_current else f"Năm {int(year)}"
        
        fig.add_trace(go.Scatter(
            x=df_year[subject_col], y=df_year['count'],
            mode='lines',
            name=name_label,
            line=line_style,
            opacity=opacity,
            hovertemplate=f"Năm {int(year)}<br>Điểm: %{{x}}<br>Số lượng: %{{y}}<extra></extra>"
        ))

    fig.update_layout(
        height=400,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(title="Điểm số", dtick=1, range=[-0.25, 10.25], showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(title="Số lượng thí sinh", showgrid=True, gridcolor='#f0f0f0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified"
    )
    return fig

# ==========================================
# CÁC HÀM RENDER & HỖ TRỢ
# ==========================================
def render(df):
    # --------------------------------------
    # 1. CSS STYLING
    # --------------------------------------
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 98%; }
        
        .dash-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; }
        .dash-title { margin: 0; font-size: 25px !important; font-weight: 700; letter-spacing: 1px;}
        .dash-subtitle { margin: 0; font-size: 13px; color: #A0AEC0;}

        .chart-banner {
            background-color: #14357A; color: white;
            padding: 8px 15px; font-size: 13px; font-weight: 600;
            border-radius: 4px 4px 0 0; 
            margin-bottom: -25px;
            position: relative; z-index: 10;
        }
    
        .kpi-card {
            background-color: white; 
            border-left: 4px solid #14357A; /* Viền trái cho giống Tab 1 */
            padding: 10px 5px; 
            border-radius: 4px; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center; 
            margin-bottom: 10px;
        }
        .kpi-title { 
            font-size: 11px; color: #555; font-weight: 600; 
            margin-bottom: 2px; text-transform: uppercase;
        }
        .kpi-value { 
            font-size: 22px; color: #14357A; font-weight: 900; margin: 0; 
        }        
        </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 2. HEADER
    # --------------------------------------
    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">📈 CHI TIẾT MÔN HỌC</h1>
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
        st.markdown(f"""
            <div style="background-color: #F0F8FF; color: #051039; padding: 0px 15px; border-radius: 4px; font-size: 13.5px; margin-top: 28px; border: 1px solid #BEE3F8; border-left: 4px solid #14357A; display: flex; align-items: center; height: 39px;">
                <span>Đang xem: <b>{selected_subject_name}</b> (Năm <b>{selected_year}</b>)</span>
            </div>
        """, unsafe_allow_html=True)

    # Tách dữ liệu
    df_year = df[df['nam'] == selected_year]
    subject_data_year = df_year[df_year[subject_col].notna()][subject_col]

    # --------------------------------------
    # 4. KPI CARDS
    # --------------------------------------
    if not subject_data_year.empty:
        total_students = len(subject_data_year)
        avg_score = subject_data_year.mean()
        med_score = subject_data_year.median()
        pass_rate = (len(subject_data_year[subject_data_year >= 5]) / total_students) * 100

        k1, k2, k3, k4 = st.columns(4, gap="small")
        k1, k2, k3, k4 = st.columns(4, gap="small")
        with k1:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">👥 Tổng thí sinh thi</div><div class="kpi-value">{total_students:,}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">📍 Điểm Trung bình</div><div class="kpi-value">{avg_score:.2f}</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">⚖️ Điểm Trung vị</div><div class="kpi-value">{med_score:.2f}</div></div>', unsafe_allow_html=True)
        with k4:
            st.markdown(f'<div class="kpi-card"><div class="kpi-title">✅ Tỷ lệ điểm ≥ 5</div><div class="kpi-value">{pass_rate:.1f}%</div></div>', unsafe_allow_html=True)


    # --------------------------------------
    # 5. CHART GRID
    # --------------------------------------
    col_left, col_right = st.columns([1, 1.2], gap="small")

    with col_left:
        st.markdown(f'<div class="chart-banner">📊 Phổ điểm chi tiết môn {selected_subject_name} ({selected_year})</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_histogram(df_year, subject_col), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown(f'<div class="chart-banner">📦 Dải điểm phân hóa môn {selected_subject_name} ({selected_year})</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_subject_boxplot(df_year, subject_col, selected_year), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(f'<div class="chart-banner">📈 So sánh xu hướng phổ điểm môn {selected_subject_name} (Hiện tại vs Quá khứ)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)   
    st.plotly_chart(plot_score_line_trend(df, subject_col, selected_year), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
