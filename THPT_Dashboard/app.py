import streamlit as st
import modules.utils
from modules.data_loader import load_data
from modules.preprocess import add_province, add_khoi_thi
from tabs import tab1_overview, tab2_score_dist, tab3_comb, tab4_geo, tab5_analysis
from modules.chatbot import render_sidebar_chatbot
# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Hệ thống Phân tích THPT", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL UI STYLING (THEME & COMPACT)
# ==========================================
st.markdown("""
    <style>
    /* 1. Background toàn bộ ứng dụng */
    .stApp {
        background: linear-gradient(180deg, #E0F7FA 0%, #80DEEA 100%);
    }


    /* 2. Tối ưu không gian nội dung chính */
    .block-container { 
        padding-top: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        max-width: 100% !important; 
    }

    
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* ----------------------------------- */
    /* STYLING SIDEBAR (DARK BLUE THEME)   */
    /* ----------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #051039 !important;
        border-right: 1px solid #14357A;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    
    /* Khóa Sidebar: Ẩn nút đóng/mở để giữ layout cố định */
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Style các nút menu điều hướng */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 10px 15px;
        background-color: #14357A;
        border-radius: 6px;
        margin-bottom: 6px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #2D5A9E;
        border: 1px solid #6FA8DC;
    }

    [data-testid="stSidebar"] hr {
        border-color: #14357A;
        margin: 10px 0px;
    }
    
    
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
        text-overflow: ellipsis;
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
    # 3. LOAD DATA
    # ==========================================
    with st.spinner("Đang kết nối hệ thống dữ liệu..."):
        df_raw, df_mavung = load_data("data/processed")
        if df_raw.empty:
            st.error("Không thể tải dữ liệu. Vui lòng kiểm tra thư mục data.")
            st.stop()
            
        df = add_province(df_raw, df_mavung)
        df = add_khoi_thi(df)

    # ==========================================
    # 4. SIDEBAR NAVIGATION
    # ==========================================
    st.sidebar.markdown("""
        <div style='text-align: center; padding-bottom: 15px;'>
            <h2 style='margin-bottom: 0; font-size: 20px;'>🎓 Phân tích Điểm thi THPT Quốc gia (2020-2025)</h2>
            <p style='color: #6FA8DC !important; font-size: 12px;'>Hệ thống Quản lý Dữ liệu</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_tab = st.sidebar.radio(
        "MENU",
        [
            "📊 Toàn Cảnh Kỳ Thi",
            "📈 Chi Tiết Môn Học",
            "🎓 Tổ Hợp Xét Tuyển",
            "🗺️ Phân Tích Địa Lý",
            "💡 Tương Quan & Phân Hóa"
        ],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # System Metadata
    st.sidebar.markdown(f"""
        <div style='font-size: 12px; opacity: 0.8;'>
            <b>🗄️ Số bản ghi:</b> {len(df):,}<br>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # CHATBOT IN SIDEBAR
    # ==========================================
    render_sidebar_chatbot()
    
        
    # ==========================================
    # 5. ROUTING
    # ==========================================
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

if __name__ == "__main__":
    main()