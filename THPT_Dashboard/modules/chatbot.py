import streamlit as st
from google import genai
import os

# ==========================================
# CÁC HÀM KHỞI TẠO & HỖ TRỢ
# ==========================================
def init_ai_client():
    if "GEMINI_API_KEY" not in st.secrets: 
        return None
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def load_system_prompt():
    path = "ai_instruction.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: 
            return f.read()
    return "Bạn là trợ lý phân tích dữ liệu chuyên nghiệp."

# ==========================================
# LOGIC LÕI VÀ GIAO DIỆN CHATBOT (BÊN TRONG POPOVER)
# ==========================================
@st.fragment(run_every=2) # Tự nhận ảnh mới từ dashboard mỗi 2 giây
def chatbot_inner_logic():
    # --- CSS MESSENGER / TELEGRAM STYLE ---
    st.markdown("""
        <style>
        /* Nền tảng Popover mềm mại hơn */
        div[data-testid="stPopoverBody"] { 
            min-width: 550px !important; 
            background-color: #F8FAFC !important; /* Xám xanh cực nhạt */
            padding: 15px !important;
        }

        /* Xóa background mặc định của container chat */
        div[data-testid="stChatMessage"] { background-color: transparent !important; }
        
        /* Ẩn avatar mặc định */
        div[data-testid="stChatMessageAvatar"] { display: none !important; }

        /* BONG BÓNG NGƯỜI DÙNG (BÊN PHẢI - MÀU GRADIENT) */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageUser"]) > div:nth-child(2) {
            background: linear-gradient(135deg, #0084FF 0%, #00C6FF 100%) !important;
            color: white !important;
            border-radius: 20px 20px 4px 20px !important;
            padding: 10px 18px !important;
            margin-left: auto !important; /* Ép bong bóng sát lề phải */
            width: fit-content !important; 
            max-width: 85% !important;
            box-shadow: 0 4px 10px rgba(0, 132, 255, 0.2) !important;
        }

        /* BONG BÓNG AI (BÊN TRÁI - MÀU TRẮNG SÁNG) */
        div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAssistant"]) > div:nth-child(2) {
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            border-radius: 20px 20px 20px 4px !important;
            padding: 10px 18px !important;
            margin-right: auto !important; /* Ép bong bóng sát lề trái */
            width: fit-content !important;
            max-width: 85% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
            border: 1px solid #E2E8F0 !important;
        }

        /* Custom nút Hủy chọn ảnh */
        .btn-cancel {
            background-color: #F1F5F9 !important; color: #EF4444 !important;
            border: 1px solid #FECACA !important; border-radius: 8px !important;
            padding: 5px 15px !important; font-size: 13px !important; font-weight: bold;
        }
        .btn-cancel:hover { background-color: #FEE2E2 !important; }
        </style>
    """, unsafe_allow_html=True)

    if "CHAT_HISTORY" not in st.session_state:
        st.session_state.CHAT_HISTORY = []

    client = init_ai_client()
    target_data = st.session_state.get("AI_VISION_TARGET", None)

    # 1. KHU VỰC NGỮ CẢNH (UI FILE ĐÍNH KÈM)
    if target_data:
        meta = target_data["metadata"]
        # Thẻ hiển thị ảnh nổi bật, có viền bo tròn
        st.markdown("<div style='background: white; padding: 12px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; margin-bottom: 15px;'>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2.5])
        with c1:
            st.image(target_data["image"], use_container_width=True)
        with c2:
            st.markdown(f"**📎 Biểu đồ đính kèm**")
            if meta.get("x_label") and meta.get("y_label"):
                st.markdown(f"<span style='color:#64748B; font-size:13px;'>Trục Y: {meta['y_label']}<br>Trục X: {meta['x_label']}</span>", unsafe_allow_html=True)
            
            # Nút gỡ ảnh gọn gàng
            if st.button("✖ Gỡ ảnh", key="remove_img", use_container_width=False):
                st.session_state.AI_VISION_TARGET = None
                st.rerun(scope="fragment")
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("💡 Chưa có biểu đồ nào. Hãy chọn 'Phân tích' dưới một biểu đồ để bắt đầu.")

    # 2. KHUNG HIỂN THỊ TIN NHẮN
    chat_box = st.container(height=450)
    with chat_box:
        # Màn hình chào mừng nếu chưa có tin nhắn
        if not st.session_state.CHAT_HISTORY:
            st.markdown("""
                <div style="text-align: center; color: #94A3B8; padding-top: 50px;">
                    <h3 style="color: #64748B;">👋 Xin chào!</h3>
                    <p>Tôi là trợ lý AI chuyên phân tích số liệu.<br>Bạn muốn hỏi gì về biểu đồ này?</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.CHAT_HISTORY:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    # 3. THANH NHẬP LIỆU (NATIVE CHAT INPUT CỦA STREAMLIT)
    if u_msg := st.chat_input("Hỏi AI (VD: Nhận xét xu hướng điểm số...)", key="chat_input"):
        if not target_data:
            st.warning("Vui lòng đính kèm một biểu đồ trước khi hỏi.")
            st.rerun(scope="fragment")
            
        # Lưu tin nhắn user
        st.session_state.CHAT_HISTORY.append({"role": "user", "content": u_msg})
        with chat_box:
            with st.chat_message("user"): 
                st.markdown(u_msg)
            
            # Khối xử lý của AI Assistant
            with st.chat_message("assistant"):
                with st.spinner("AI đang phân tích biểu đồ..."):
                    try:
                        sys_prompt = load_system_prompt()
                        meta = target_data["metadata"]
                        
                        full_prompt = f"""
                        {sys_prompt}
                        
                        DỮ LIỆU ĐANG XEM:
                        - Biểu đồ đo lường: {meta.get('y_label', 'Không rõ')}
                        - Phân loại theo: {meta.get('x_label', 'Không rõ')}
                        
                        CÂU HỎI: {u_msg}
                        """
                        
                        res = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[full_prompt, target_data["image"]]
                        )
                        st.markdown(res.text)
                        st.session_state.CHAT_HISTORY.append({"role": "assistant", "content": res.text})
                    except Exception as e:
                        st.error(f"Lỗi kết nối AI: {e}")
        
        st.rerun(scope="fragment")

    # 4. NÚT DỌN DẸP LỊCH SỬ CHAT
    if st.session_state.CHAT_HISTORY:
        st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
        if st.button("🧹 Xóa lịch sử trò chuyện", type="tertiary"):
            st.session_state.CHAT_HISTORY = []
            st.rerun(scope="fragment")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# RENDER POPOVER RA SIDEBAR CHÍNH
# ==========================================
def render_sidebar_chatbot():
    st.sidebar.markdown("""
        <style>
        /* CSS Nút Popover ngoài Sidebar */
        .stPopover { width: 100%; }
        
        .stPopover button {
            background-color: #253D70 !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            height: 48px !important;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
            border-radius: 10px !important;
        }

        .stPopover button:hover {
            background-color: #3D5AFE !important; 
            border-color: #ffffff !important; 
            box-shadow: 0 5px 15px rgba(61, 90, 254, 0.4) !important; 
            transform: translateY(-2px);
        }

        .stPopover button:active {
            transform: translateY(0px);
            box-shadow: 0 2px 5px rgba(61, 90, 254, 0.2) !important;
        }

        .stPopover button * { 
            color: white !important; 
            fill: white !important; 
            transition: all 0.3s ease !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Reset counter để đảm bảo ID nút chụp ảnh ở các tab không bị trùng lặp
        st.session_state.chart_counter = 0 
        
        st.markdown("---")
        with st.popover("✨ Trợ lý AI", use_container_width=True):
            chatbot_inner_logic()