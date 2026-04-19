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

@st.cache_data(max_entries=1)
def get_correlation_matrix(df, year):
    """Tính toán ma trận tương quan giữa các môn học"""
    df_y = df[df['nam'] == year][list(SUBJECT_NAMES.keys())]
    df_y = df_y.rename(columns=SUBJECT_NAMES)
    corr_matrix = df_y.corr().fillna(0)
    return corr_matrix

@st.cache_data(max_entries=1)
def get_hn_hcm_comparison(df, year):
    """So sánh HN và HCM dựa trên mapping tên chính xác"""
    df_y = df[df['nam'] == year]
    city_mapping = {'Ha Noi': 'Hà Nội', 'TP. Ho Chi Minh': 'TP. Hồ Chí Minh'}
    res = []
    subs = ['toan', 'ngu_van', 'ngoai_ngu']
    for s in subs:
        for raw_name, display_name in city_mapping.items():
            d_city_sub = df_y[df_y['Ten Tinh'] == raw_name][s].dropna()
            if not d_city_sub.empty:
                res.append({
                    'Thành phố': display_name, 'Môn': SUBJECT_NAMES[s], 
                    'Điểm TB': d_city_sub.mean(), 
                    'Tỷ lệ Giỏi': (d_city_sub >= 8).mean() * 100
                })
    return pd.DataFrame(res) if res else pd.DataFrame(columns=['Thành phố', 'Môn', 'Điểm TB', 'Tỷ lệ Giỏi'])

@st.cache_data(max_entries=1)
def get_violin_data(df, year):
    """Chuẩn bị dữ liệu cho Violin Plot (Lấy mẫu để tối ưu tốc độ)"""
    df_y = df[df['nam'] == year][list(SUBJECT_NAMES.keys())]
    
    # Lấy mẫu 50,000 bản ghi để trình duyệt không bị treo khi vẽ vĩ cầm
    if len(df_y) > 50000:
        df_y = df_y.sample(50000, random_state=42)
        
    df_melt = df_y.melt(var_name='Môn', value_name='Điểm').dropna()
    df_melt['Môn'] = df_melt['Môn'].map(SUBJECT_NAMES)
    return df_melt

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ
# ==========================================

def plot_correlation_heatmap(corr_matrix):
    fig = px.imshow(
        corr_matrix, text_auto='.2f', aspect="auto",
        color_continuous_scale='RdBu_r', range_color=[-1, 1]
    )
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10))
    return fig

def plot_dumbbell_chart(df_hn_hcm):
    if df_hn_hcm.empty: return px.bar().update_layout(height=400)
    fig = go.Figure()
    colors = {'Hà Nội': '#14357A', 'TP. Hồ Chí Minh': '#E67C22'}
    for sub in df_hn_hcm['Môn'].unique():
        df_sub = df_hn_hcm[df_hn_hcm['Môn'] == sub]
        if len(df_sub) == 2:
            vals = df_sub.set_index('Thành phố')['Điểm TB']
            fig.add_trace(go.Scatter(x=[vals['Hà Nội'], vals['TP. Hồ Chí Minh']], y=[sub, sub], mode='lines', line=dict(color='#CBD5E1', width=4), showlegend=False))
            for city in ['Hà Nội', 'TP. Hồ Chí Minh']:
                row = df_sub[df_sub['Thành phố'] == city].iloc[0]
                fig.add_trace(go.Scatter(x=[row['Điểm TB']], y=[sub], mode='markers', name=city, marker=dict(color=colors[city], size=15), showlegend=sub==df_hn_hcm['Môn'].unique()[0], hovertemplate=f"<b>{city}</b><br>Điểm TB: {row['Điểm TB']:.2f}<extra></extra>"))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), plot_bgcolor='white')
    return fig

def plot_violin_chart(df_melt):
    """Vẽ biểu đồ vĩ cầm cho 9 môn học"""
    fig = px.violin(
        df_melt, x='Môn', y='Điểm', color='Môn',
        box=True, # Hiển thị hộp (Boxplot) bên trong vĩ cầm
        points=False, # Không vẽ từng điểm để tránh lag
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(
        height=500, margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(title="Thang điểm", gridcolor='#F0F0F0', range=[-0.5, 10.5]),
        xaxis=dict(title=""), showlegend=False
    )
    return fig

# ==========================================
# MAIN RENDER FUNCTION
# ==========================================
def render(df):
    st.markdown("""
        <style>
        .dash-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 15px; }
        .dash-title { margin: 0; font-size: 25px !important; font-weight: 700; letter-spacing: 1px;}
        .chart-banner { background-color: #14357A; color: white; padding: 5px 15px; font-size: 13px; font-weight: 600; border-radius: 4px 4px 0 0; }
        .chart-container { background-color: white; padding: 15px; border-radius: 0 0 4px 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 15px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">💡 TƯƠNG QUAN & PHÂN HÓA</h1>
            <p class="dash-subtitle">Phân tích sự tương quan và cấu trúc điểm số của kỳ thi THPT Quốc gia</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_year = st.selectbox("📅 Chọn Năm phân tích", sorted(df['nam'].unique(), reverse=True), key='tab5_year')

    # HÀNG 1: HEATMAP & DUMBBELL
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

    # HÀNG 2: VIOLIN PLOT (Toàn bộ chiều ngang)
    st.markdown('<div class="chart-banner">🎻 Hình dáng Phổ điểm & Độ phân hóa (Violin Plot)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    with st.spinner("Đang vẽ biểu đồ vĩ cầm..."):
        df_violin = get_violin_data(df, selected_year)
        st.plotly_chart(plot_violin_chart(df_violin), use_container_width=True)
    st.markdown('<p style="font-size:12px; color:#666; font-style:italic;">* Biểu đồ vĩ cầm hiển thị mật độ thí sinh ở từng mức điểm. "Bụng" càng to thì thí sinh tập trung ở đó càng nhiều.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # HÀNG 3: CÔNG CỤ TƯƠNG TÁC
    with st.expander("🛠️ Khám phá Hệ số Tương quan (Pearson Correlation)"):
        r_val = st.slider("Hệ số r:", -1.0, 1.0, 0.8, 0.05)
        np.random.seed(42)
        x = np.random.randn(200)
        y = r_val * x + np.sqrt(1 - r_val**2) * np.random.randn(200)
        fig_sim = px.scatter(x=x, y=y, trendline="ols" if r_val != 0 else None, opacity=0.6).update_layout(height=300, plot_bgcolor='white', xaxis_showticklabels=False, yaxis_showticklabels=False)
        st.plotly_chart(fig_sim, use_container_width=True)