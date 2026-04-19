import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ
# ==========================================
def plot_trend_area(df_full):
    """Biểu đồ vùng: Quy mô thí sinh qua các năm (Dữ liệu toàn cục)"""
    trend = df_full.groupby('nam')['sbd'].count().reset_index()
    trend.columns = ['Năm', 'Thí sinh']
    
    fig = px.area(
        trend, x='Năm', y='Thí sinh', markers=True,
        color_discrete_sequence=['#14357A'] 
    )
    fig.update_layout(
        height=300,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=10, t=10, b=0),
        xaxis=dict(tickmode='linear', showgrid=True, gridcolor='#f0f0f0', title=""),
        yaxis=dict(tickformat=',', showgrid=True, gridcolor='#f0f0f0', title="")
    )
    return fig

def plot_avg_bar(df_filtered):
    """Biểu đồ cột ngang: Điểm trung bình các môn (Dữ liệu đã lọc)"""
    subjects = {
        'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
        'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
    }
    avail_subs = [s for s in subjects.keys() if s in df_filtered.columns]
    
    if not avail_subs or df_filtered.empty: 
        return go.Figure().update_layout(height=300, title="Không có dữ liệu")
    
    means = df_filtered[avail_subs].mean().reset_index()
    means.columns = ['Môn', 'Điểm TB']
    means['Môn'] = means['Môn'].map(subjects)
    means = means.sort_values('Điểm TB', ascending=True)
    
    fig = px.bar(
        means, x='Điểm TB', y='Môn', orientation='h', text_auto='.2f',
        color_discrete_sequence=['#2D5A9E']
    )
    fig.update_layout(
        height=300,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=20, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="", visible=False),
        yaxis=dict(title="")
    )
    return fig

def plot_top_provinces(df_filtered):
    """Biểu đồ cột ngang: Top 5 địa phương (Dữ liệu đã lọc)"""
    if df_filtered.empty:
        return go.Figure().update_layout(height=300)
        
    col_name = 'Ten Tinh' if 'Ten Tinh' in df_filtered.columns else 'Ma'
    top_prov = df_filtered[col_name].value_counts().nlargest(5).reset_index()
    top_prov.columns = ['Tỉnh/Thành', 'Số lượng']
    top_prov = top_prov.sort_values('Số lượng', ascending=True)
    
    fig = px.bar(
        top_prov, x='Số lượng', y='Tỉnh/Thành', orientation='h', text_auto=',',
        color_discrete_sequence=['#14357A']
    )
    fig.update_layout(
        height=300,
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(l=0, r=20, t=10, b=0),
        xaxis=dict(showgrid=False, title="", visible=False),
        yaxis=dict(title="")
    )
    return fig


# ==========================================
# MAIN RENDER FUNCTION
# ==========================================
def render(df, global_year=None):
    # 1. CSS STYLING
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; padding-bottom: 0.5rem; max-width: 98%; }
        .ss-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; }
        .ss-title { margin: 0; font-size: 25px !important; font-weight: 700; letter-spacing: 1px;}
        .ss-subtitle { margin: 0; font-size: 16px; color: #A0AEC0;}
        
        .kpi-card {
            background-color: white; border-left: 4px solid #14357A;
            padding: 10px 5px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center; margin-bottom: 15px;
        }
        .kpi-title { font-size: 11px; color: #555; font-weight: 600; margin-bottom: 2px; text-transform: uppercase;}
        .kpi-value { font-size: 22px; color: #14357A; font-weight: 900; margin: 0; }
        
        .chart-banner {
            background-color: #14357A; color: white;
            padding: 5px 15px; font-size: 13px; font-weight: 600;
            border-radius: 4px 4px 0 0; margin-bottom: 0px;
        }
        .chart-container {
            background-color: white; padding: 10px;
            border-radius: 0 0 4px 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. HEADER
    st.markdown("""
        <div class="ss-header">
            <h1 class="ss-title">📊 TOÀN CẢNH KỲ THI</h1>
            <div class="ss-subtitle">Phân tích quy mô thí sinh & Xu hướng điểm số và cơ cấu ban ngành toàn quốc</div>
        </div>
    """, unsafe_allow_html=True)

    # 3. FILTER BAR (3 Cột Dropdown)
    st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 2px; color: #14357A;'>🎛️ Bộ lọc Tổng hợp</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3, gap="small")
    
    with f_col1:
        years = ['Tất cả'] + sorted(df['nam'].dropna().unique().tolist(), reverse=True)
        selected_year = st.selectbox("📅 Năm thi", years, key='tab1_year')
        
    with f_col2:
        provinces = ['Tất cả'] + sorted(df['Ten Tinh'].dropna().unique().tolist()) if 'Ten Tinh' in df.columns else ['Tất cả']
        selected_prov = st.selectbox("📍 Tỉnh / Thành", provinces, key='tab1_prov')
        
    with f_col3:
        blocks = ['Tất cả', 'KHTN', 'KHXH']
        selected_block = st.selectbox("📚 Khối thi", blocks, key='tab1_block')

    # Logic Filter
    df_filtered = df.copy()
    if selected_year != 'Tất cả':
        df_filtered = df_filtered[df_filtered['nam'] == selected_year]
    if selected_prov != 'Tất cả':
        df_filtered = df_filtered[df_filtered['Ten Tinh'] == selected_prov]
    if selected_block != 'Tất cả':
        df_filtered = df_filtered[df_filtered['khoi_thi'] == selected_block]

    # 4. KPI CARDS (3 Cột)
    total_students = len(df_filtered)
    khtn_cnt = len(df_filtered[df_filtered['khoi_thi'] == 'KHTN'])
    khxh_cnt = len(df_filtered[df_filtered['khoi_thi'] == 'KHXH'])
    pct_khtn = (khtn_cnt / total_students * 100) if total_students > 0 else 0
    pct_khxh = (khxh_cnt / total_students * 100) if total_students > 0 else 0
    
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">👥 Tổng Thí Sinh (Đã lọc)</div><div class="kpi-value">{total_students:,}</div></div>', unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">🔬 Tỷ lệ Ban KHTN</div><div class="kpi-value">{pct_khtn:.1f}%</div></div>', unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">📖 Tỷ lệ Ban KHXH</div><div class="kpi-value">{pct_khxh:.1f}%</div></div>', unsafe_allow_html=True)

    # 5. CHART GRID (3 Biểu đồ trên 1 hàng ngang)
    c1, c2, c3 = st.columns(3, gap="small")
    
    with c1:
        st.markdown('<div class="chart-banner">📈 Quy mô thí sinh toàn quốc</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_trend_area(df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-banner">📊 Điểm trung bình các môn học</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_avg_bar(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="chart-banner">🏆 Các địa phương tiêu biểu</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_top_provinces(df_filtered), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)