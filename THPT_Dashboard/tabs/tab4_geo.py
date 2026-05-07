import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os

# ==========================================
# CẤU HÌNH & MAPPING
# ==========================================
SUBJECT_MAP = {
    'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
    'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
    'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
}

# ==========================================
# LOAD GEOJSON (DỮ LIỆU BẢN ĐỒ)
# ==========================================
@st.cache_data # Sử dụng cache của Streamlit để không phải load lại file JSON nhiều lần
def load_geojson():
    # Xác định đường dẫn tương đối trỏ tới file vn_geo.json chứa ranh giới 63 tỉnh thành
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/processed', 'vn_geo.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

# ==========================================
# CÁC HÀM VẼ BIỂU ĐỒ
# ==========================================
def plot_choropleth_map(df_year, subject_col, geojson_data):
    """Hàm vẽ bản đồ nhiệt (Choropleth) phân bố số lượng điểm 9-10"""
    # Xử lý lỗi nếu không đọc được file bản đồ
    if geojson_data is None:
        return px.bar(title="⚠️ Không tìm thấy file").update_layout(height=500)

    # 1. Lấy danh sách 63 tỉnh từ CHÍNH FILE JSON
    all_names = [feature['properties']['name'] for feature in geojson_data['features']]
    all_provinces = pd.DataFrame({'Ten Tinh': all_names})
    
    # 2. Lọc ra các học sinh đạt điểm xuất sắc (>= 9) và đếm số lượng theo từng tỉnh
    df_high = df_year[df_year[subject_col] >= 9]
    counts = df_high.groupby('Ten Tinh').size().reset_index(name='Số lượng 9-10')
    
    # 3. Gộp dữ liệu (Left Join): Ghép số lượng điểm cao vào danh sách 63 tỉnh
    # Tỉnh nào không có ai đạt >=9 sẽ bị NaN, sau đó fillna(0) để hiện màu nhạt nhất
    map_data = pd.merge(all_provinces, counts, on='Ten Tinh', how='left')
    map_data['Số lượng 9-10'] = map_data['Số lượng 9-10'].fillna(0)
    
    # 4. Vẽ bản đồ bằng Plotly Express
    fig = px.choropleth(
        map_data,
        geojson=geojson_data,
        locations='Ten Tinh', # Cột chứa tên tỉnh trong DataFrame
        featureidkey='properties.name', # Khóa chứa tên tỉnh trong file GeoJSON
        color='Số lượng 9-10', # Giá trị dùng để tô màu
        color_continuous_scale='Blues', # Thang màu xanh dương
        hover_name='Ten Tinh' # Tên hiện lên khi di chuột vào
    )
    
    # =========================================================
    # GHIM TỌA ĐỘ HOÀNG SA & TRƯỜNG SA (SCATTERGEO)
    # =========================================================
    # Vẽ thêm 2 điểm Scatter lên bản đồ để hiển thị quần đảo Hoàng Sa và Trường Sa
    fig.add_trace(go.Scattergeo(
        lon=[112.0, 114.2], 
        lat=[16.5, 9.8],    
        text=['<b>QĐ Hoàng Sa</b><br>(Đà Nẵng)', '<b>QĐ Trường Sa</b><br>(Khánh Hòa)'],
        mode='markers+text',
        textposition='bottom center',
        textfont=dict(size=11, color='#14357A'),
        marker=dict(size=6, color='#E67C22', symbol='square'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Giới hạn góc nhìn (camera) của bản đồ tập trung vào khu vực Việt Nam
    fig.update_geos(
        visible=False, # Ẩn các bản đồ thế giới mặc định
        center=dict(lat=16.1, lon=109.0), 
        lataxis_range=[8.5, 23.5], 
        lonaxis_range=[102.0, 118.5]
    )
    
    # Chỉnh sửa layout, lề và thanh chú thích màu sắc
    fig.update_layout(
        height=695,
        margin=dict(l=0, r=0, t=0, b=0), 
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_colorbar=dict(
            title="SL 9-10đ",
            thickness=15,
            len=0.5,
            yanchor="middle",
            y=0.5,
            x=0.05 
        )
    )
    return fig

def plot_top_avg(df_year, subject_col):
    """Biểu đồ ngang Top 10 tỉnh có điểm TB cao nhất"""
    # Tính điểm trung bình theo tỉnh, lấy 10 tỉnh cao nhất
    top_avg = df_year.groupby('Ten Tinh')[subject_col].mean().nlargest(10).reset_index()
    top_avg.columns = ['Tỉnh/Thành', 'Điểm TB']
    top_avg = top_avg.sort_values('Điểm TB', ascending=True) # Sort ngược để tỉnh Top 1 hiển thị trên cùng biểu đồ
    
    fig = px.bar(
        top_avg, x='Điểm TB', y='Tỉnh/Thành', orientation='h', text_auto='.2f',
        color_discrete_sequence=['#14357A']
    )
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(visible=False), yaxis=dict(title="") # Ẩn trục X cho gọn vì đã có text trên cột
    )
    return fig

def plot_top_ratio(df_year, subject_col):
    """Biểu đồ ngang Top 10 tỉnh có Tỷ lệ điểm >= 8 cao nhất"""
    # Lấy các dòng có điểm (bỏ NaN) để tính toán chính xác
    df_valid = df_year[df_year[subject_col].notna()]
    
    # Tính tổng thí sinh thi môn này theo tỉnh
    total_by_prov = df_valid.groupby('Ten Tinh').size()
    
    # Tính số thí sinh đạt điểm giỏi (>= 8) theo tỉnh
    high_by_prov = df_valid[df_valid[subject_col] >= 8].groupby('Ten Tinh').size()
    
    # Gộp 2 series trên và tính phần trăm
    ratio_df = pd.DataFrame({'Tổng': total_by_prov, 'Giỏi': high_by_prov}).fillna(0)
    ratio_df['Tỷ lệ %'] = (ratio_df['Giỏi'] / ratio_df['Tổng']) * 100
    
    # Lấy Top 10 tỉnh có tỷ lệ cao nhất và sắp xếp
    top_ratio = ratio_df.nlargest(10, 'Tỷ lệ %').reset_index()
    top_ratio = top_ratio.sort_values('Tỷ lệ %', ascending=True)
    
    fig = px.bar(
        top_ratio, x='Tỷ lệ %', y='Ten Tinh', orientation='h', 
        text=top_ratio['Tỷ lệ %'].apply(lambda x: f"{x:.1f}%"), # Format số hiện trên cột có dấu %
        color_discrete_sequence=['#6FA8DC'] # Màu xanh nhạt để phân biệt với chart trên
    )
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=20, t=10, b=0),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(visible=False, range=[0, max(top_ratio['Tỷ lệ %']) * 1.15]), # Nới rộng trục X khoảng 15% để chữ ko bị lẹm
        yaxis=dict(title="")
    )
    return fig

# ==========================================
# MAIN RENDER FUNCTION (HÀM GỌI GIAO DIỆN)
# ==========================================
def render(df):
    geojson_data = load_geojson()

    # 1. CSS STYLING
    # Khối tùy chỉnh giao diện (Màu sắc, kích thước, banner, shadow...)
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

    # 2. HEADER
    # Tiêu đề của Tab 4
    st.markdown("""
        <div class="dash-header">
            <h1 class="dash-title">🗺️ PHÂN TÍCH ĐỊA LÝ</h1>
            <p class="dash-subtitle">Phân tích sự phân hóa chất lượng giáo dục theo không gian địa lý</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. FILTER BAR (BỘ LỌC)
    st.markdown("<div style='font-size: 14px; font-weight: bold; margin-bottom: 2px; color: #14357A;'>🎛️ Bộ lọc Phân tích</div>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns([1, 1, 1.5], gap="small")
    
    with f_col1:
        # Danh sách năm thi lấy từ dữ liệu thực, sort giảm dần
        years = sorted([int(y) for y in df['nam'].dropna().unique()], reverse=True)
        selected_year = st.selectbox("📅 Chọn Năm thi", years)
        
    with f_col2:
        # Chọn môn học bằng tên tiếng Việt, sau đó dịch ngược lại thành tên cột trong df
        selected_subject_name = st.selectbox("🎯 Chọn Môn học", list(SUBJECT_MAP.values()))
        subject_col = [k for k, v in SUBJECT_MAP.items() if v == selected_subject_name][0]
    
    with f_col3:
        # Bảng hiển thị thông báo trạng thái hiện tại đang xem thông tin gì
        st.markdown(f"""
            <div style="background-color: #F0F8FF; color: #051039; padding: 0px 15px; border-radius: 4px; font-size: 13.5px; margin-top: 28px; border: 1px solid #BEE3F8; border-left: 4px solid #14357A; display: flex; align-items: center; height: 39px;">
                <span>Đang xem: <b>Môn {selected_subject_name}</b> (Năm {selected_year})</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

    # Tách dữ liệu của năm được chọn
    df_year = df[df['nam'] == selected_year]

    # ==========================================
    # 4. KPI CARDS (TÍNH TOÁN CÁC THÔNG SỐ TỔNG QUAN)
    # ==========================================
    # Lấy các điểm hợp lệ (không null) của môn đang chọn
    valid_scores = df_year[subject_col].dropna()
    
    # Khởi tạo giá trị nếu có dữ liệu
    if len(valid_scores) > 0:
        total_9_10 = (valid_scores >= 9).sum()
        avg_score = valid_scores.mean()
        total_ge_8 = (valid_scores >= 8).sum()
        ratio_ge_8 = (total_ge_8 / len(valid_scores)) * 100
    else:
        # Tránh lỗi chia cho 0 nếu không có dữ liệu
        total_9_10 = 0
        avg_score = 0.0
        ratio_ge_8 = 0.0

    kpi1, kpi2, kpi3 = st.columns(3)
    
    # Render các thẻ thông tin (SL điểm cao, Điểm TB, Tỷ lệ giỏi)
    with kpi1:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">🌟 Tổng SL 9-10 điểm</div>
                <div class="kpi-value">{total_9_10:,}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">📊 Điểm TB Cả nước</div>
                <div class="kpi-value">{avg_score:.2f}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with kpi3:
        st.markdown(f'''
            <div class="kpi-card">
                <div class="kpi-title">🎯 Tỷ lệ Điểm Giỏi (≥ 8)</div>
                <div class="kpi-value">{ratio_ge_8:.2f}%</div>
            </div>
        ''', unsafe_allow_html=True)

    # ==========================================
    # 5. LAYOUT: BẢN ĐỒ (Trái) - BIỂU ĐỒ TOP 10 (Phải)
    # ==========================================
    # Tạo 2 cột với tỷ lệ 1.5 : 1 (Bản đồ chiếm nhiều không gian hơn)
    col_map, col_charts = st.columns([1.5, 1], gap="small")

    with col_map:
        # Render bản đồ địa lý bên cột trái
        st.markdown(f'<div class="chart-banner">📍 Mật độ Thí sinh đạt Điểm Xuất Sắc (9-10đ)</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_choropleth_map(df_year, subject_col, geojson_data), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_charts:
        # Chart trên: Top 10 Tỉnh Điểm trung bình cao nhất
        st.markdown(f'<div class="chart-banner">🏆 Top 10 Địa phương: Điểm TB cao nhất</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_top_avg(df_year, subject_col), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Chart dưới: Top 10 Tỉnh có Tỷ lệ điểm >= 8 cao nhất
        st.markdown(f'<div class="chart-banner">🎯 Top 10 Địa phương: Tỷ lệ Điểm Giỏi (≥ 8) cao nhất</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(plot_top_ratio(df_year, subject_col), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)