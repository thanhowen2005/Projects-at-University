import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ==========================================
# CẤU HÌNH & MAPPING
# ==========================================
SUBJECT_NAMES = {
    'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
    'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
    'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
}

# ==========================================
# CÁC HÀM XỬ LÝ DỮ LIỆU
# ==========================================

@st.cache_data(max_entries=1) # Lưu cache để tăng tốc độ tính toán
def get_correlation_matrix(df, year):
    """Tính toán ma trận tương quan (Pearson) giữa các môn học"""
    # Lọc dữ liệu theo năm và chỉ lấy các cột môn học
    df_y = df[df['nam'] == year][list(SUBJECT_NAMES.keys())]
    df_y = df_y.rename(columns=SUBJECT_NAMES)
    # Tính ma trận tương quan, điền 0 nếu không có dữ liệu (ví dụ giữa KHTN và KHXH)
    corr_matrix = df_y.corr().fillna(0)
    return corr_matrix

@st.cache_data(max_entries=1)
def get_hn_hcm_comparison(df, year):
    """So sánh điểm trung bình của Hà Nội và TP.HCM"""
    df_y = df[df['nam'] == year]
    city_mapping = {'Ha Noi': 'Hà Nội', 'TP. Ho Chi Minh': 'TP. Hồ Chí Minh'}
    res = []
    subs = ['toan', 'ngu_van', 'ngoai_ngu'] # Chỉ so sánh 3 môn chính
    
    for s in subs:
        for raw_name, display_name in city_mapping.items():
            # Lấy điểm của môn học tương ứng theo từng thành phố
            d_city_sub = df_y[df_y['Ten Tinh'] == raw_name][s].dropna()
            if not d_city_sub.empty:
                res.append({
                    'Thành phố': display_name, 'Môn': SUBJECT_NAMES[s], 
                    'Điểm TB': d_city_sub.mean(), 
                })
    return pd.DataFrame(res) if res else pd.DataFrame(columns=['Thành phố', 'Môn', 'Điểm TB'])

@st.cache_data(max_entries=1)
def get_quadrant_data(df, year):
    """Tính toán Điểm TB (Độ khó) và Độ lệch chuẩn (Tính phân hóa) của 9 môn"""
    df_y = df[df['nam'] == year][list(SUBJECT_NAMES.keys())]
    
    stats = []
    for col, name in SUBJECT_NAMES.items():
        data = df_y[col].dropna()
        if not data.empty:
            stats.append({
                'Môn': name,
                'Điểm TB': data.mean(),
                'Độ lệch chuẩn': data.std(),
                'Số lượng thi': len(data)
            })
    return pd.DataFrame(stats)

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ
# ==========================================

def plot_correlation_heatmap(corr_matrix):
    """Vẽ biểu đồ nhiệt (Heatmap) thể hiện ma trận tương quan"""
    fig = px.imshow(
        corr_matrix, text_auto='.2f', aspect="auto",
        color_continuous_scale='RdBu_r', range_color=[-1, 1] # Thang màu Đỏ (âm) - Trắng (0) - Xanh dương (dương)
    )
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10))
    return fig

def plot_dumbbell_chart(df_hn_hcm):
    """Vẽ biểu đồ quả tạ (Dumbbell) so sánh khoảng cách điểm giữa 2 thành phố"""
    if df_hn_hcm.empty: return px.bar().update_layout(height=400)
    fig = go.Figure()
    colors = {'Hà Nội': '#14357A', 'TP. Hồ Chí Minh': '#E67C22'}
    
    for sub in df_hn_hcm['Môn'].unique():
        df_sub = df_hn_hcm[df_hn_hcm['Môn'] == sub]
        if len(df_sub) == 2:
            vals = df_sub.set_index('Thành phố')['Điểm TB']
            # Vẽ đường thẳng nối giữa 2 điểm (cán tạ)
            fig.add_trace(go.Scatter(x=[vals['Hà Nội'], vals['TP. Hồ Chí Minh']], y=[sub, sub], mode='lines', line=dict(color='#CBD5E1', width=4), showlegend=False))
            # Vẽ 2 điểm tròn ở 2 đầu (quả tạ)
            for city in ['Hà Nội', 'TP. Hồ Chí Minh']:
                row = df_sub[df_sub['Thành phố'] == city].iloc[0]
                fig.add_trace(go.Scatter(x=[row['Điểm TB']], y=[sub], mode='markers', name=city, marker=dict(color=colors[city], size=15), showlegend=sub==df_hn_hcm['Môn'].unique()[0], hovertemplate=f"<b>{city}</b><br>Điểm TB: {row['Điểm TB']:.2f}<extra></extra>"))
                
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), plot_bgcolor='white')
    return fig


def plot_quadrant_chart(df_stats):
    """Vẽ biểu đồ phân tán (Góc phần tư) đánh giá chất lượng đề thi"""
    if df_stats.empty: return go.Figure()

    # Tính điểm cắt (Trung vị) để làm mốc chia 4 góc phần tư
    x_mid = df_stats['Điểm TB'].median()
    y_mid = df_stats['Độ lệch chuẩn'].median()

    fig = px.scatter(
        df_stats, 
        x='Điểm TB', 
        y='Độ lệch chuẩn', 
        text='Môn',              # Hiện tên môn học
        size='Số lượng thi',      # Bong bóng to/nhỏ theo số lượng thí sinh
        color='Môn',
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # Thêm trục tọa độ chéo (Crosshair) chia 4 vùng
    fig.add_hline(y=y_mid, line_dash="dot", line_color="#A0AEC0", 
                  annotation_text="Trung bình Phân hóa", annotation_position="bottom right")
    fig.add_vline(x=x_mid, line_dash="dot", line_color="#A0AEC0", 
                  annotation_text="Trung bình Độ khó", annotation_position="top left")

    # Thêm nhãn mô tả ý nghĩa cho từng góc phần tư
    fig.add_annotation(x=df_stats['Điểm TB'].max(), y=df_stats['Độ lệch chuẩn'].max(), text="Đề Dễ & Phân hóa tốt", showarrow=False, opacity=0.3, font=dict(size=14, color="#2CA02C"))
    fig.add_annotation(x=df_stats['Điểm TB'].min(), y=df_stats['Độ lệch chuẩn'].min(), text="Đề Khó & Kém phân hóa", showarrow=False, opacity=0.3, font=dict(size=14, color="#D62728"))
    fig.add_annotation(x=df_stats['Điểm TB'].max(), y=df_stats['Độ lệch chuẩn'].min(), text="Lạm phát điểm", showarrow=False, opacity=0.3, font=dict(size=14, color="#FF7F0E"))
    fig.add_annotation(x=df_stats['Điểm TB'].min(), y=df_stats['Độ lệch chuẩn'].max(), text="Lọc học sinh giỏi", showarrow=False, opacity=0.3, font=dict(size=14, color="#14357A"))

    fig.update_layout(
        height=500, margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(title="Điểm Trung Bình (Độ khó giảm dần →)", showgrid=True, gridcolor='#F0F8FF'),
        yaxis=dict(title="Độ Lệch Chuẩn (Tính phân hóa tăng dần ↑)", showgrid=True, gridcolor='#F0F8FF'),
        showlegend=False
    )
    
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    return fig

# ==========================================
# MAIN RENDER FUNCTION
# ==========================================
def render(df):
    # Định dạng giao diện bằng CSS (Banner, Khung viền, Title)
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
        /* CSS cho các ô KPI */
        .kpi-card {
            background-color: white;
            border-left: 4px solid #14357A;
            padding: 8px 5px; 
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
            margin-bottom: 10px; 
        }
        .kpi-title { 
            font-size: 14px;
            color: #555; 
            font-weight: 600; 
            margin-bottom: 2px; 
            text-transform: uppercase;
        }
        .kpi-value { 
            font-size: 20px;
            color: #14357A; 
            font-weight: 900; 
            margin: 0; 
        }
        </style>
    """, unsafe_allow_html=True)

    # Tiêu đề chính của Tab
    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">💡 TƯƠNG QUAN & PHÂN HÓA</h1>
            <p class="dash-subtitle">Phân tích sự tương quan và cấu trúc điểm số của kỳ thi THPT Quốc gia</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Bộ lọc năm thi
    selected_year = st.selectbox("📅 Chọn Năm phân tích", sorted(df['nam'].unique(), reverse=True), key='tab5_year')

    # HÀNG 1: Chia 2 cột cho Ma trận tương quan (Heatmap) & Đối chuẩn (Dumbbell)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-banner">🧬 Ma trận Tương quan Môn học</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_correlation_heatmap(get_correlation_matrix(df, selected_year)), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="chart-banner">⚖️ Đối chuẩn Hà Nội vs TP.HCM</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_dumbbell_chart(get_hn_hcm_comparison(df, selected_year)), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # HÀNG 2: Biểu đồ Góc phần tư (Quadrant Chart) chiếm toàn bộ chiều ngang
    st.markdown('<div class="chart-banner">🎯 Ma trận Đánh giá Đề thi: Độ khó vs. Độ phân hóa</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    df_quadrant = get_quadrant_data(df, selected_year)
    st.plotly_chart(plot_quadrant_chart(df_quadrant), use_container_width=True)
    
    # Ghi chú hướng dẫn đọc biểu đồ góc phần tư
    st.markdown("""
        <div style="font-size:13px; color:#555; background-color:#F8FAFC; padding:10px; border-radius:5px; border-left:3px solid #14357A; margin-top:10px;">
            <b>💡 Hướng dẫn đọc ma trận:</b><br>
            • <b>Trục ngang (Điểm TB):</b> Môn nằm càng về bên phải thì đề thi càng dễ.<br>
            • <b>Trục dọc (Độ lệch chuẩn):</b> Môn nằm càng lên cao thì tính phân loại học sinh càng tốt.<br>
            • Kích thước bong bóng thể hiện số lượng thí sinh dự thi.
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # HÀNG 3: CÔNG CỤ TƯƠNG TÁC (Giả lập hệ số tương quan Pearson)
    with st.expander("🛠️ Khám phá Hệ số Tương quan (Pearson Correlation)"):
        r_val = st.slider("Hệ số r:", -1.0, 1.0, 0.8, 0.05) # Thanh kéo chọn giá trị r
        np.random.seed(42)
        # Tạo dữ liệu giả lập dựa trên hệ số r được chọn
        x = np.random.randn(200)
        y = r_val * x + np.sqrt(1 - r_val**2) * np.random.randn(200)
        
        # Vẽ biểu đồ phân tán (Scatter) để trực quan hóa mức độ liên kết
        fig_sim = px.scatter(x=x, y=y, trendline="ols" if r_val != 0 else None, opacity=0.6).update_layout(height=300, plot_bgcolor='white', xaxis_showticklabels=False, yaxis_showticklabels=False)
        st.plotly_chart(fig_sim, use_container_width=True)