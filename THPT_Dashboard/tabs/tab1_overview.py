import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# ==========================================
# BỘ MÀU CHUẨN CHO 3 KHỐI THI
# ==========================================
BLOCK_COLORS = {
    'KHTN': '#14357A',                     # Xanh Navy 
    'KHXH': '#FF7F0E',                     # Cam
    'Thi không đầy đủ tổ hợp': '#CBD5E1'   # Xám nhạt
}

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ
# ==========================================
def plot_trend_area(df_full):
    trend = df_full.groupby('nam')['sbd'].count().reset_index()
    trend.columns = ['Năm', 'Thí sinh']
    fig = px.area(trend, x='Năm', y='Thí sinh', markers=True, color_discrete_sequence=['#14357A'])
    fig.update_layout(
        height=320, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=10, t=10, b=0),
        xaxis=dict(tickmode='linear', showgrid=True, gridcolor='#f0f0f0', title="Năm"),
        yaxis=dict(tickformat=',', showgrid=True, gridcolor='#f0f0f0', title="Số lượng thí sinh")
    )
    return fig

def plot_avg_bar(df_filtered):
    subjects = {
        'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
        'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
    }
    avail_subs = [s for s in subjects.keys() if s in df_filtered.columns]
    if not avail_subs or df_filtered.empty: return go.Figure().update_layout(height=320, title="Không có dữ liệu")
    
    means = df_filtered[avail_subs].mean().reset_index()
    means.columns = ['Môn', 'Điểm TB']
    means['Môn'] = means['Môn'].map(subjects)
    means = means.sort_values('Điểm TB', ascending=True)
    
    fig = px.bar(means, x='Điểm TB', y='Môn', orientation='h', text_auto='.2f', color_discrete_sequence=['#2D5A9E'])
    fig.update_layout(
        height=320, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=20, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0', title="Điểm trung bình", visible=False),
        yaxis=dict(title="Môn")
    )
    return fig

def plot_top_provinces(df_filtered):
    if df_filtered.empty: return go.Figure().update_layout(height=320)
    col_name = 'Ten Tinh' if 'Ten Tinh' in df_filtered.columns else 'Ma'
    top_prov = df_filtered[col_name].value_counts().nlargest(5).reset_index()
    top_prov.columns = ['Tỉnh/Thành', 'Số lượng']
    top_prov = top_prov.sort_values('Số lượng', ascending=True)
    
    fig = px.bar(top_prov, x='Số lượng', y='Tỉnh/Thành', orientation='h', text_auto=',', color_discrete_sequence=['#14357A'])
    fig.update_layout(
        height=320, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=0, r=20, t=10, b=0),
        xaxis=dict(showgrid=False, title="Số lượng", visible=False),
        yaxis=dict(title="Tỉnh thành")
    )
    return fig

def plot_block_donut(df_filtered):
    """Biểu đồ Donut: Cơ cấu 3 nhóm khối thi"""
    if df_filtered.empty: return go.Figure()
    
    counts = df_filtered['khoi_thi'].value_counts().reset_index()
    counts.columns = ['Khối thi', 'Số lượng']

    fig = px.pie(
        counts, values='Số lượng', names='Khối thi', 
        hole=0.55, color='Khối thi', color_discrete_map=BLOCK_COLORS
    )
    fig.update_layout(
        height=350, margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, title="")
    )
    fig.update_traces(textposition='inside', textinfo='percent', showlegend=False)
    return fig

def plot_block_structure_stacked(df_full, selected_prov):
    """Biểu đồ 100% Stacked Bar: Xu hướng chuyển dịch cơ cấu lịch sử"""
    df_plot = df_full.copy()
    if selected_prov != 'Tất cả':
        df_plot = df_plot[df_plot['Ten Tinh'] == selected_prov]
    
    df_plot = df_plot[df_plot['nam'].notna()]
    if df_plot.empty: return go.Figure()

    grouped = df_plot.groupby(['nam', 'khoi_thi']).size().reset_index(name='count')
    total_year = grouped.groupby('nam')['count'].transform('sum')
    grouped['pct'] = (grouped['count'] / total_year) * 100
    
    grouped = grouped.sort_values('nam')
    grouped['nam'] = grouped['nam'].astype(int).astype(str)
    
    # Cập nhật danh sách sắp xếp 3 nhóm
    cat_order = ['KHTN', 'KHXH', 'Thi không đầy đủ tổ hợp']

    fig = px.bar(
        grouped, x='nam', y='pct', color='khoi_thi', barmode='stack',
        text=grouped['pct'].apply(lambda x: f"{x:.1f}%" if x > 4 else ""), 
        color_discrete_map=BLOCK_COLORS, category_orders={'khoi_thi': cat_order}
    )

    fig.update_layout(
        height=350, plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Năm thi", showgrid=False),
        yaxis=dict(title="Tỷ lệ cơ cấu (%)", range=[0, 100], showgrid=False, visible=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title="")
    )
    fig.update_traces(textposition='inside', textfont_size=12, textfont_color='white')
    return fig

# ==========================================
# MAIN RENDER
# ==========================================
def render(df, global_year=None):
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem; padding-bottom: 0.5rem; max-width: 98%; }
        .ss-header { background-color: #051039; color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 10px; }
        .ss-title { margin: 0; font-size: 25px !important; font-weight: 700; letter-spacing: 1px;}
        .ss-subtitle { margin: 0; font-size: 16px; color: #A0AEC0;}
        .chart-banner {
            background-color: #14357A; color: white;
            padding: 8px 15px; font-size: 13px; font-weight: 600;
            border-radius: 4px 4px 0 0; margin-bottom: -25px;
            position: relative; z-index: 10;
        }
        </style>
    """, unsafe_allow_html=True)

    # HEADER
    st.markdown("""
        <div class="ss-header">
            <h1 class="ss-title">📊 TOÀN CẢNH KỲ THI</h1>
            <div class="ss-subtitle">Phân tích quy mô thí sinh & Xu hướng chuyển dịch cơ cấu khối thi</div>
        </div>
    """, unsafe_allow_html=True)

    # FILTER BAR (3 Cột)
    st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 2px; color: #14357A;'>🎛️ Bộ lọc Phân tích</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3, gap="small")
    
    with f_col1:
        years = ['Tất cả'] + sorted(df['nam'].dropna().unique().tolist(), reverse=True)
        selected_year = st.selectbox("📅 Năm thi", years, key='tab1_year')
        
    with f_col2:
        provinces = ['Tất cả'] + sorted(df['Ten Tinh'].dropna().unique().tolist()) if 'Ten Tinh' in df.columns else ['Tất cả']
        selected_prov = st.selectbox("📍 Tỉnh / Thành", provinces, key='tab1_prov')
        
    with f_col3:
        blocks = ['Tất cả', 'KHTN', 'KHXH', 'Thi không đầy đủ tổ hợp']
        selected_block = st.selectbox("📚 Khối thi", blocks, key='tab1_block')

    # Xử lý Lọc Dữ Liệu
    df_filtered = df.copy()
    if selected_year != 'Tất cả':
        df_filtered = df_filtered[df_filtered['nam'] == selected_year]
    if selected_prov != 'Tất cả':
        df_filtered = df_filtered[df_filtered['Ten Tinh'] == selected_prov]
    if selected_block != 'Tất cả':
        df_filtered = df_filtered[df_filtered['khoi_thi'] == selected_block]

    # Hiển thị nhanh Tổng Thí Sinh
    st.markdown(f"<div style='margin-bottom:15px; font-size:15px; color:#333;'>Thống kê dựa trên <b>{len(df_filtered):,}</b> thí sinh.</div>", unsafe_allow_html=True)

    # ---------------------------------------------
    # HÀNG 1: 3 BIỂU ĐỒ TỔNG QUAN
    # ---------------------------------------------
    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        st.markdown('<div class="chart-banner">📈 Quy mô thí sinh toàn quốc</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_trend_area(df), use_container_width=True)

    with c2:
        st.markdown('<div class="chart-banner">📊 Điểm trung bình các môn học</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_avg_bar(df_filtered), use_container_width=True)

    with c3:
        st.markdown('<div class="chart-banner">🏆 Các địa phương tiêu biểu</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_top_provinces(df_filtered), use_container_width=True)

    st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)

    # ---------------------------------------------
    # HÀNG 2: PHÂN TÍCH CHUYỂN DỊCH CƠ CẤU KHỐI THI
    # ---------------------------------------------
    st.markdown('<div class="chart-banner">⚖️ PHÂN TÍCH CƠ CẤU KHỐI THI</div>', unsafe_allow_html=True)
    col_donut, col_stack = st.columns([1, 2], gap="small")
    
    with col_donut:
        st.markdown('<div style="text-align:center; font-size:13px; font-weight:bold; color:#14357A; margin-top:35px; margin-bottom:-10px;">CƠ CẤU NĂM ĐANG CHỌN</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_block_donut(df_filtered), use_container_width=True)
        
    with col_stack:
        st.markdown('<div style="text-align:center; font-size:13px; font-weight:bold; color:#14357A; margin-top:35px; margin-bottom:-10px;">XU HƯỚNG CHUYỂN DỊCH QUA CÁC NĂM</div>', unsafe_allow_html=True)
        st.plotly_chart(plot_block_structure_stacked(df, selected_prov), use_container_width=True)