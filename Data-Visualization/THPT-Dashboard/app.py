import streamlit as st
from modules.data_loader import load_data
from modules.preprocess import add_province, add_khoi_thi
from tabs import tab1_overview, tab2_score_dist, tab3_placeholder, tab4_placeholder

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="THPT Exam Analytics", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL UI STYLING (THEME & COMPACT)
# ==========================================
st.markdown("""
    <style>
    /* 1. Background toàn bộ ứng dụng (Xám bạc nhẹ) */
    .stApp {
        background: linear-gradient(180deg, #F5F7FA 0%, #EEF1F5 100%);
    }

    /* 2. Tối ưu không gian nội dung chính */
    .block-container { 
        padding-top: 0rem !important; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
        max-width: 100% !important; 
    }

    /* Ẩn header mặc định để giao diện sạch hơn */
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
    </style>
""", unsafe_allow_html=True)

def main():
    # ==========================================
    # 3. LOAD DATA
    # ==========================================
    with st.spinner("Đang kết nối hệ thống dữ liệu..."):
        df_raw, df_mavung = load_data("Data-Visualization/THPT-Dashboard/data/processed")
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
            <h2 style='margin-bottom: 0; font-size: 20px;'>🎓 THPT ANALYTICS</h2>
            <p style='color: #6FA8DC !important; font-size: 12px;'>Management Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    selected_tab = st.sidebar.radio(
        "MENU",
        [
            "📊 Executive Summary",
            "📈 Score Distribution",
            "🗺️ Regional Performance",
            "🧠 Advanced Insights"
        ],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # System Metadata
    st.sidebar.markdown(f"""
        <div style='font-size: 12px; opacity: 0.8;'>
            <b>🗄️ Records:</b> {len(df):,}<br>
            <b>🔄 Status:</b> Connected
        </div>
    """, unsafe_allow_html=True)
    
    # Profile Card
    st.sidebar.markdown("""
        <div style='margin-top: 50px; padding: 10px; background-color: #14357A; border-radius: 6px; display: flex; align-items: center;'>
            <div style='background-color: white; color: #051039 !important; width: 30px; height: 30px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; margin-right: 10px;'>A</div>
            <div style='font-size: 13px;'>Admin User</div>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 5. ROUTING
    # ==========================================
    if selected_tab == "📊 Executive Summary":
        tab1_overview.render(df) 
    elif selected_tab == "📈 Score Distribution":
        tab2_score_dist.render(df)
    elif selected_tab == "🗺️ Regional Performance":
        tab3_placeholder.render(df)
    elif selected_tab == "🧠 Advanced Insights":
        tab4_placeholder.render(df)

if __name__ == "__main__":
    main()