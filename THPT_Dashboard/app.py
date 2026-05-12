import streamlit as st
import modules.utils
from modules.data_loader import load_data
from modules.preprocess import add_province, add_khoi_thi
from tabs import tab1_overview, tab2_score_dist, tab3_comb, tab4_geo, tab5_analysis
from modules.chatbot import render_sidebar_chatbot

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
# Cài đặt các thông số cơ bản cho trang web như tiêu đề, biểu tượng và giao diện rộng
st.set_page_config(
    page_title="Hệ thống Phân tích THPT", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded" # Luôn mở thanh menu bên trái
)

# ==========================================
# 2. TÙY CHỈNH GIAO DIỆN (CSS)
# ==========================================
# Dùng CSS để làm đẹp giao diện, đổi màu nền và tùy chỉnh thanh menu bên trái
st.markdown("""
    <style>
    /* 1. Đổi màu nền cho toàn bộ ứng dụng */
    .stApp {
        background: linear-gradient(180deg, #E0F7FA 0%, #80DEEA 100%);
    }

    /* 2. Căn chỉnh lề để tận dụng tối đa không gian màn hình */
    .block-container { 
        padding-top: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        max-width: 100% !important; 
    }
    
    /* Ẩn phần header và menu mặc định của Streamlit*/
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* ----------------------------------- */
    /* TÙY CHỈNH THANH MENU BÊN TRÁI (SIDEBAR) */
    /* ----------------------------------- */
    /* Đổi nền sidebar thành màu xanh đen */
    [data-testid="stSidebar"] {
        background-color: #051039 !important;
        border-right: 1px solid #14357A;
    }
    
    /* Chữ trong sidebar đổi thành màu trắng */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Ẩn nút đóng/mở sidebar để cố định menu không cho người dùng ẩn đi */
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Làm đẹp các nút chọn trang (Menu) */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 10px 15px;
        background-color: #14357A;
        border-radius: 6px;
        margin-bottom: 6px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    
    /* Đổi màu nút menu khi di chuột vào */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #2D5A9E;
        border: 1px solid #6FA8DC;
    }

    /* Đổi màu đường gạch ngang phân cách trong sidebar */
    [data-testid="stSidebar"] hr {
        border-color: #14357A;
        margin: 10px 0px;
    }
    
    /* Chỉnh sửa kích thước và định dạng chữ cho các nút menu */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        width: 100%;
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 10px 14px;
        box-sizing: border-box;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis; /* Hiện dấu ... nếu chữ quá dài */
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        margin: 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        transform: none;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # ==========================================
    # 3. TẢI VÀ XỬ LÝ DỮ LIỆU
    # ==========================================
    # Hiển thị vòng xoay chờ trong lúc đọc dữ liệu lên
    with st.spinner("Đang kết nối hệ thống dữ liệu..."):
        # Lấy dữ liệu từ thư mục
        df_raw, df_mavung = load_data("data/processed")
        
        # Báo lỗi và dừng chương trình nếu file trống hoặc không tìm thấy
        if df_raw.empty:
            st.error("Không thể tải dữ liệu. Vui lòng kiểm tra thư mục data.")
            st.stop()
            
        # Thêm tên tỉnh và phân loại khối thi vào bảng dữ liệu
        df = add_province(df_raw, df_mavung)
        df = add_khoi_thi(df)

    # ==========================================
    # 4. TẠO MENU ĐIỀU HƯỚNG TRÊN SIDEBAR
    # ==========================================
    # Tiêu đề của thanh menu
    st.sidebar.markdown("""
        <div style='text-align: center; padding-bottom: 15px;'>
            <h2 style='margin-bottom: 0; font-size: 20px;'>🎓 Phân tích Điểm thi THPT Quốc gia (2020-2024)</h2>
            <p style='color: #6FA8DC !important; font-size: 12px;'>Hệ thống Quản lý Dữ liệu</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tạo các nút radio để người dùng chọn trang muốn xem
    selected_tab = st.sidebar.radio(
        "MENU",
        [
            "📊 Toàn Cảnh Kỳ Thi",
            "📈 Chi Tiết Môn Học",
            "🎓 Tổ Hợp Xét Tuyển",
            "🗺️ Phân Tích Địa Lý",
            "💡 Tương Quan & Phân Hóa"
        ],
        label_visibility="collapsed" # Ẩn tên nhóm radio
    )
    
    st.sidebar.markdown("---")
    
    # Hiển thị thông tin tổng quát (tổng số lượng thí sinh/bản ghi)
    st.sidebar.markdown(f"""
        <div style='font-size: 12px; opacity: 0.8;'>
            <b>🗄️ Số bản ghi:</b> {len(df):,}<br>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # TÍCH HỢP CHATBOT AI VÀO SIDEBAR
    # ==========================================
    # Gọi hàm hiển thị giao diện Chatbot
    render_sidebar_chatbot()
        
    # ==========================================
    # 5. CHUYỂN HƯỚNG TRANG (ROUTING)
    # ==========================================
    # Dựa vào tên trang người dùng click trên menu để gọi file xử lý tương ứng
    if selected_tab == "📊 Toàn Cảnh Kỳ Thi":
        tab1_overview.render(df) 
    elif selected_tab == "📈 Chi Tiết Môn Học":
        tab2_score_dist.render(df)
    elif selected_tab == "🎓 Tổ Hợp Xét Tuyển":
        tab3_comb.render(df)
    elif selected_tab == "🗺️ Phân Tích Địa Lý":
        tab4_geo.render(df)
    elif selected_tab == "💡 Tương Quan & Phân Hóa":
        tab5_analysis.render(df)

# Chạy ứng dụng
if __name__ == "__main__":
    main()