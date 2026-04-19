import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ (CHART COMPONENTS)
# (Đã tắt title mặc định của Plotly để dùng Banner HTML)
# ==========================================
def plot_trend_area(df_full):
    trend = df_full.groupby('nam')['sbd'].count().reset_index()
    trend.columns = ['Năm', 'Thí sinh']
    
    fig = px.area(
        trend, x='Năm', y='Thí sinh', markers=True,
        color_discrete_sequence=['#14357A'] # Xanh đậm Super Store
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(tickmode='linear', showgrid=True, gridcolor='#f0f0f0', title=""),
        yaxis=dict(tickformat=',', showgrid=True, gridcolor='#f0f0f0', title="")
    )
    return fig

def plot_avg_bar(df_filtered):
    subjects = {
        'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
        'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
    }
    avail_subs = [s for s in subjects.keys() if s in df_filtered.columns]
    
    if not avail_subs: return go.Figure()
    
    means = df_filtered[avail_subs].mean().reset_index()
    means.columns = ['Môn', 'Điểm TB']
    means['Môn'] = means['Môn'].map(subjects)
    means = means.sort_values('Điểm TB', ascending=True)
    
    fig = px.bar(
        means, x='Điểm TB', y='Môn', orientation='h', text_auto='.2f',
        color_discrete_sequence=['#2D5A9E']
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=20, t=10, b=10),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="", visible=False),
        yaxis=dict(title="")
    )
    return fig

def plot_block_donut(df_filtered):
    blocks = df_filtered['khoi_thi'].value_counts().reset_index()
    blocks.columns = ['Khối', 'Số lượng']
    
    fig = px.pie(
        blocks, names='Khối', values='Số lượng', hole=0.5,
        color='Khối', color_discrete_map={'KHTN': '#14357A', 'KHXH': '#6FA8DC'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10), showlegend=False
    )
    return fig

def plot_score_trend(df_full):
    main_subs = ['toan', 'ngu_van', 'ngoai_ngu']
    avail_subs = [s for s in main_subs if s in df_full.columns]
    
    if not avail_subs: return go.Figure()
        
    trend = df_full.groupby('nam')[avail_subs].mean().reset_index()
    trend = trend.melt(id_vars='nam', var_name='Môn', value_name='Điểm TB')
    
    sub_map = {'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ'}
    trend['Môn'] = trend['Môn'].map(sub_map)
    
    fig = px.line(
        trend, x='nam', y='Điểm TB', color='Môn', markers=True,
        color_discrete_sequence=['#14357A', '#E67C22', '#2D5A9E']
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(tickmode='linear', showgrid=True, gridcolor='#f0f0f0', title=""),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title=""),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def plot_top_provinces(df_filtered):
    col_name = 'Ten Tinh' if 'Ten Tinh' in df_filtered.columns else 'Ma'
    
    top_prov = df_filtered[col_name].value_counts().nlargest(5).reset_index()
    top_prov.columns = ['Tỉnh/Thành', 'Số lượng']
    top_prov = top_prov.sort_values('Số lượng', ascending=True)
    
    fig = px.bar(
        top_prov, x='Số lượng', y='Tỉnh/Thành', orientation='h', text_auto=',',
        color_discrete_sequence=['#14357A']
    )
    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=10, r=20, t=10, b=10),
        xaxis=dict(showgrid=False, title="", visible=False),
        yaxis=dict(title="")
    )
    return fig


# ==========================================
# MAIN RENDER FUNCTION
# ==========================================
def render(df, global_year=None):
    # --------------------------------------
    # 1. CSS STYLING (SUPER STORE THEME)
    # --------------------------------------
    st.markdown("""
        <style>
        /* Reset background chung của Streamlit */
        .stApp { background-color: #F0F2F6; }
        .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 95%; }
        
        /* 1. Header giống ảnh */
        .ss-header {
            background-color: #051039;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .ss-title { margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 1px;}
        
        /* 2. KPI Cards giống ảnh (Có viền xanh đậm ở trên) */
        .kpi-wrapper { display: flex; gap: 15px; margin-bottom: 20px; }
        .kpi-card {
            background: white;
            flex: 1;
            padding: 15px;
            border-radius: 4px;
            border-top: 4px solid #051039; /* Viền xanh đậm */
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        }
        .kpi-icon { font-size: 35px; margin-right: 15px; }
        .kpi-details { display: flex; flex-direction: column; }
        .kpi-label { font-size: 13px; color: #555; font-weight: 600; text-transform: uppercase; }
        .kpi-val { font-size: 26px; color: #14357A; font-weight: 700; }
        
        /* 3. Chart Banners (Banner tiêu đề xanh đậm) */
        .chart-banner {
            background-color: #14357A;
            color: white;
            padding: 8px 15px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 4px 4px 0 0;
            margin-bottom: 0px;
        }
        .chart-container {
            background-color: white;
            padding: 10px;
            border-radius: 0 0 4px 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 2. HEADER
    # --------------------------------------
    st.markdown("""
        <div class="ss-header">
            <h1 class="ss-title">🎓 THPT EXAM DASHBOARD</h1>
            <div style="font-size:14px; border: 1px solid white; padding: 5px 15px;">Executive Summary</div>
        </div>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 3. FILTER BAR 
    # --------------------------------------
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        years = ['Tất cả'] + sorted(df['nam'].dropna().unique().tolist(), reverse=True)
        # Ưu tiên lấy year từ global filter ở sidebar nếu có, nếu không thì mặc định
        default_idx = years.index(global_year) if global_year in years else 0
        selected_year = st.selectbox("Năm thi", years, index=default_idx)
        
    with f_col2:
        provinces = ['Tất cả'] + sorted(df['Ten Tinh'].dropna().unique().tolist()) if 'Ten Tinh' in df.columns else ['Tất cả']
        selected_prov = st.selectbox("Tỉnh / Thành", provinces)
        
    with f_col3:
        blocks = ['Tất cả', 'KHTN', 'KHXH']
        selected_block = st.selectbox("Khối thi", blocks)
        
    with f_col4:
        st.write("") # Dùng để căn chỉnh layout
        st.markdown("<div style='margin-top: 30px; font-weight:bold; color:#14357A;'>Lọc Dữ Liệu 📌</div>", unsafe_allow_html=True)

    # Thực thi Logic Filter
    df_filtered = df.copy()
    if selected_year != 'Tất cả':
        df_filtered = df_filtered[df_filtered['nam'] == selected_year]
    if selected_prov != 'Tất cả':
        df_filtered = df_filtered[df_filtered['Ten Tinh'] == selected_prov]
    if selected_block != 'Tất cả':
        df_filtered = df_filtered[df_filtered['khoi_thi'] == selected_block]

    # --------------------------------------
    # 4. KPI CARDS (HTML TRỰC TIẾP GIỐNG ẢNH)
    # --------------------------------------
    total_students = len(df_filtered)
    khtn_cnt = len(df_filtered[df_filtered['khoi_thi'] == 'KHTN'])
    khxh_cnt = len(df_filtered[df_filtered['khoi_thi'] == 'KHXH'])
    pct_khtn = (khtn_cnt / total_students * 100) if total_students > 0 else 0
    pct_khxh = (khxh_cnt / total_students * 100) if total_students > 0 else 0
    
    core_subs = [s for s in ['toan', 'ngu_van', 'ngoai_ngu'] if s in df_filtered.columns]
    avg_overall = df_filtered[core_subs].mean().mean() if (core_subs and not df_filtered[core_subs].empty) else 0.0

    st.markdown(f"""
        <div class="kpi-wrapper">
            <div class="kpi-card">
                <div class="kpi-icon">👥</div>
                <div class="kpi-details">
                    <div class="kpi-label">Tổng Thí Sinh</div>
                    <div class="kpi-val">{total_students:,}</div>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-details">
                    <div class="kpi-label">Điểm TB (Toán, Văn, Anh)</div>
                    <div class="kpi-val">{avg_overall:.2f}</div>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon">🔬</div>
                <div class="kpi-details">
                    <div class="kpi-label">Thí sinh KHTN</div>
                    <div class="kpi-val">{pct_khtn:.1f}%</div>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon">📖</div>
                <div class="kpi-details">
                    <div class="kpi-label">Thí sinh KHXH</div>
                    <div class="kpi-val">{pct_khxh:.1f}%</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 5. CHART GRID CÓ BANNER XANH ĐẬM
    # --------------------------------------
    
    # Hàng 1
    r1_col1, r1_col2, r1_col3 = st.columns([1.2, 1, 1])
    
    with r1_col1:
        st.markdown('<div class="chart-banner">Quy mô thí sinh dự thi qua các năm</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_trend_area(df), use_container_width=True) # Full trend
        st.markdown('</div>', unsafe_allow_html=True)

    with r1_col2:
        st.markdown('<div class="chart-banner">Điểm trung bình các môn học</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_avg_bar(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r1_col3:
        st.markdown('<div class="chart-banner">Tỷ lệ đăng ký Khối thi (%)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_block_donut(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Hàng 2
    r2_col1, r2_col2 = st.columns(2)
    
    with r2_col1:
        st.markdown('<div class="chart-banner">Xu hướng Điểm trung bình 3 môn cốt lõi</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_score_trend(df), use_container_width=True) # Full trend
        st.markdown('</div>', unsafe_allow_html=True)

    with r2_col2:
        st.markdown('<div class="chart-banner">Top 5 Địa phương có quy mô lớn nhất</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_top_provinces(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)