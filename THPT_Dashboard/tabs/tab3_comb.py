import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# CẤU HÌNH TỔ HỢP MÔN
# ==========================================
# Định nghĩa các khối xét tuyển đại học phổ biến theo từng Ban
KHTN_BLOCKS = {
    'A00': ['toan', 'vat_ly', 'hoa_hoc'],
    'A01': ['toan', 'vat_ly', 'ngoai_ngu'],
    'A02': ['toan', 'vat_ly', 'sinh_hoc'],
    'B00': ['toan', 'hoa_hoc', 'sinh_hoc'],
    'D07': ['toan', 'hoa_hoc', 'ngoai_ngu'],
    'D08': ['toan', 'sinh_hoc', 'ngoai_ngu'],
}

KHXH_BLOCKS = {
    'C00': ['ngu_van', 'lich_su', 'dia_ly'],
    'C19': ['ngu_van', 'lich_su', 'gdcd'],
    'C20': ['ngu_van', 'dia_ly', 'gdcd'],
    'D01': ['toan', 'ngu_van', 'ngoai_ngu'],
    'D14': ['ngu_van', 'lich_su', 'ngoai_ngu'],
    'D15': ['ngu_van', 'dia_ly', 'ngoai_ngu'],
}

# Gộp chung để tiện tra cứu toàn cục
ALL_BLOCKS = {**KHTN_BLOCKS, **KHXH_BLOCKS}

SUBJECT_NAMES = {
    'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
    'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
    'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
}

# ==========================================
# CÁC HÀM XỬ LÝ DỮ LIỆU & VẼ BIỂU ĐỒ
# ==========================================
@st.cache_data(max_entries=1)
def calculate_trend_data(df):
    """Tính toán ngưỡng điểm Top 5% (Percentile 95) cho TẤT CẢ các khối thi qua các năm"""
    trend_data = []
    years = sorted(df['nam'].dropna().unique())
    
    # Lặp qua từng năm và từng khối để tìm ngưỡng điểm của nhóm thí sinh giỏi nhất
    for y in years:
        df_y = df[df['nam'] == y]
        for b_name, b_subs in ALL_BLOCKS.items():
            df_b = df_y.dropna(subset=b_subs)
            if not df_b.empty:
                totals = df_b[b_subs].sum(axis=1)
                p95 = totals.quantile(0.95) # Lấy mốc điểm phân chia 5% cao nhất
                trend_data.append({'Năm': y, 'Khối': b_name, 'Điểm Top 5%': p95})
                
    return pd.DataFrame(trend_data)

def plot_histogram(df_block, block_name):
    # Vẽ biểu đồ Histogram phân phối tổng điểm 3 môn của khối xét tuyển
    fig = px.histogram(
        df_block, 
        x='total_score', 
        nbins=60, 
        color_discrete_sequence=['#14357A'],
        labels={'total_score': 'Tổng điểm 3 môn', 'count': 'Số lượng thí sinh'}
    )
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(title="Tổng điểm", tick0=0, dtick=1, gridcolor='#F0F0F0'),
        yaxis=dict(title="Số thí sinh", gridcolor='#F0F0F0'),
        bargap=0.1
    )
    return fig

def plot_trend_line(df_trend):
    # Biểu đồ đường thể hiện mức độ cạnh tranh (điểm Top 5%) thay đổi qua các năm
    fig = px.line(
        df_trend, 
        x='Năm', y='Điểm Top 5%', color='Khối',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(title="Năm", dtick=1, gridcolor='#F0F0F0'),
        yaxis=dict(title="Điểm (Top 5%)", gridcolor='#F0F0F0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_radar_chart(df_all, df_top, block_subs):
    # Vẽ biểu đồ Radar so sánh năng lực: Điểm TB toàn nhóm vs Điểm TB nhóm Top 5%
    # 1. Tính trung bình cho nhóm ALL
    avg_all = df_all[block_subs].mean().tolist()
    # 2. Tính trung bình cho nhóm TOP 5%
    avg_top = df_top[block_subs].mean().tolist()
    
    categories = [SUBJECT_NAMES[s] for s in block_subs]
    
    # Khép kín vòng tròn radar (điểm đầu = điểm cuối)
    avg_all += avg_all[:1]
    avg_top += avg_top[:1]
    categories += categories[:1]

    fig = go.Figure()

    # Lớp 1: Trung bình tất cả thí sinh (làm nền mờ)
    fig.add_trace(go.Scatterpolar(
        r=avg_all,
        theta=categories,
        fill='toself',
        name='Trung bình chung',
        fillcolor='rgba(180, 180, 180, 0.2)',
        line=dict(color='rgba(150, 150, 150, 0.5)', width=1, dash='dash'),
    ))

    # Lớp 2: Trung bình nhóm Top 5% (in đậm, nổi bật)
    fig.add_trace(go.Scatterpolar(
        r=avg_top,
        theta=categories,
        fill='toself',
        name='Nhóm Top 5%',
        fillcolor='rgba(20, 53, 122, 0.4)',
        line=dict(color='#14357A', width=3),
        marker=dict(size=8, symbol='circle')
    ))

    fig.update_layout(
        height=380,
        margin=dict(l=50, r=50, t=40, b=20),
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 10], 
                tickfont=dict(size=10),
                gridcolor="#EEE"
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#14357A', weight='bold'),
                gridcolor="#EEE"
            )
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig


# ==========================================
# CÁC HÀM RENDER & HỖ TRỢ
# ==========================================
def render(df):
    # 1. CSS STYLING
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; padding-bottom: 0.5rem; max-width: 98%; }
        .dash-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; }
        .dash-title { margin: 0; font-size: 25px !important; font-weight: 700; letter-spacing: 1px;}
        .dash-subtitle { margin: 0; font-size: 22px; color: #A0AEC0;}
        .chart-banner {
            background-color: #14357A; color: white;
            padding: 8px 15px; font-size: 13px; font-weight: 600;
            border-radius: 4px 4px 0 0; 
            margin-bottom: -25px;
            position: relative; z-index: 10;
        }
        .kpi-card {
            background-color: white; border-left: 4px solid #14357A;
            padding: 8px 5px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center; margin-bottom: 10px;
        }
        .kpi-title { font-size: 12px; color: #555; font-weight: 600; margin-bottom: 2px; text-transform: uppercase;}
        .kpi-value { font-size: 24px; color: #14357A; font-weight: 900; margin: 0; }
        </style>
    """, unsafe_allow_html=True)

    # 2. HEADER
    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">🎓 TỔ HỢP XÉT TUYỂN</h1>
            <p class="dash-subtitle">Phân tích Phổ điểm Khối thi & Cạnh tranh Xét tuyển Đại học theo Ban</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. FILTER BAR (Thanh công cụ lọc phân tầng: Năm -> Ban -> Khối)
    st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 2px; color: #14357A;'>🎛️ Bộ lọc Phân tích</div>", unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3, f_col4 = st.columns([1, 1.2, 1, 2], gap="small")
    
    with f_col1:
        years = sorted([int(y) for y in df['nam'].dropna().unique()], reverse=True)
        selected_year = st.selectbox("📅 Năm thi", years, key='tab4_year')
        
    with f_col2:
        # Cấp 1: Chọn Ban Xét tuyển
        selected_group = st.selectbox("🎯 Ban Xét tuyển", ["Khoa học Tự nhiên (KHTN)", "Khoa học Xã hội (KHXH)"], key='tab4_group')
        
    with f_col3:
        # Cấp 2: Tự động đổi danh sách Khối dựa trên Ban đã chọn
        active_blocks = KHTN_BLOCKS if "KHTN" in selected_group else KHXH_BLOCKS
        selected_block = st.selectbox("📚 Khối thi", list(active_blocks.keys()), key='tab4_block')
        block_subs = active_blocks[selected_block]
        
    with f_col4:
        # Hiển thị các môn thành phần của khối đang chọn
        subs_text = " + ".join([SUBJECT_NAMES[s] for s in block_subs])
        st.markdown(f"""
            <div style="background-color: #F0F8FF; color: #051039; padding: 0px 15px; border-radius: 4px; font-size: 13.5px; margin-top: 28px; border: 1px solid #BEE3F8; border-left: 4px solid #14357A; display: flex; align-items: center; height: 39px;">
                <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <b>{selected_block}</b>: {subs_text}
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    # ==========================================
    # 4. DATA PROCESSING
    # ==========================================
    df_year = df[df['nam'] == selected_year]
    
    # LỌC NGHIÊM NGẶT: Loại bỏ thí sinh bị điểm liệt hoặc vắng mặt 1 trong 3 môn
    df_block = df_year.dropna(subset=block_subs).copy()
    
    # Báo lỗi nếu năm đó chưa thi hoặc dữ liệu hỏng
    if df_block.empty:
        st.warning(f"⚠️ Không có đủ dữ liệu thí sinh dự thi khối {selected_block} trong năm {selected_year}.")
        return

    # Tính tổng điểm 3 môn cho mỗi thí sinh
    df_block['total_score'] = df_block[block_subs].sum(axis=1)
    
    # Tách nhóm thí sinh Top 5% để phân tích chuyên sâu (Radar chart)
    threshold_95 = df_block['total_score'].quantile(0.95)
    df_top5 = df_block[df_block['total_score'] >= threshold_95]
    
    # Tính các chỉ số cho KPI Card
    total_students = len(df_block)
    avg_block_score = df_block['total_score'].mean()
    p95_score = df_block['total_score'].quantile(0.95)

    # Hiển thị 3 thẻ KPI
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">👥 Tổng thí sinh xét khối</div>
                <div class="kpi-value">{total_students:,}</div>
            </div>
        ''', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">📊 Điểm Trung Bình Khối</div>
                <div class="kpi-value">{avg_block_score:.2f}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">🏆 Ngưỡng điểm Top 5%</div> <div class="kpi-value">{p95_score:.2f}</div>
            </div>
        ''', unsafe_allow_html=True)

    # ==========================================
    # 5. RENDER BIỂU ĐỒ
    # ==========================================
    
    # Chart 1: Histogram (Full width)
    st.markdown(f'<div class="chart-banner">📈 Phổ điểm tổng cộng Khối {selected_block} năm {selected_year}</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(plot_histogram(df_block, selected_block), width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="small")
    
    with col_left:
        # Chart 2: Trend Line so sánh cạnh tranh trong cùng một Ban
        st.markdown(f'<div class="chart-banner">🚀 Xu hướng điểm Top 5% nội bộ Ban {"KHTN" if "KHTN" in selected_group else "KHXH"}</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        df_trend = calculate_trend_data(df) 
        df_trend_filtered = df_trend[df_trend['Khối'].isin(active_blocks.keys())]
        st.plotly_chart(plot_trend_line(df_trend_filtered), width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # Chart 3: Radar đối chuẩn môn học (Top 5% vs Average)
        st.markdown(f'<div class="chart-banner">🕸️ Đóng góp của các môn thành phần ({selected_block})</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_radar_chart(df_block, df_top5, block_subs), width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)