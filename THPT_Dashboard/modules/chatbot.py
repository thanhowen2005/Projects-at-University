import streamlit as st
from google import genai
import os

# ==========================================
# CÁC HÀM KHỞI TẠO & HỖ TRỢ
# ==========================================
def init_ai_client():
    """Khởi tạo kết nối với Google Gemini AI thông qua API Key"""
    # Kiểm tra xem API Key đã được cấu hình trong file secrets chưa
    if "GEMINI_API_KEY" not in st.secrets: 
        return None
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def load_system_prompt():
    """Đọc file cấu hình vai trò (Prompt) cho AI"""
    path = "ai_instruction.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f: 
            return f.read()
    # Nếu không có file cấu hình, dùng câu lệnh mặc định
    return "Bạn là trợ lý phân tích dữ liệu chuyên nghiệp."

# ==========================================
# LOGIC LÕI VÀ GIAO DIỆN CHATBOT (BÊN TRONG POPOVER)
# ==========================================
# Cập nhật fragment mỗi 2 giây để chatbot tự nhận diện khi có biểu đồ mới được đẩy vào
@st.fragment(run_every=2) 
def chatbot_inner_logic():
    # --- CSS MESSENGER / TELEGRAM STYLE ---
    # Tùy chỉnh giao diện đoạn chat cho giống các ứng dụng nhắn tin hiện đại
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
        
        /* Ẩn avatar mặc định của Streamlit */
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

    # Khởi tạo bộ nhớ lưu trữ lịch sử chat nếu chưa có
    if "CHAT_HISTORY" not in st.session_state:
        st.session_state.CHAT_HISTORY = []

    client = init_ai_client()
    # Lấy dữ liệu biểu đồ mà người dùng vừa chọn (được lưu ở các Tab khác)
    target_data = st.session_state.get("AI_VISION_TARGET", None)

    # 1. KHU VỰC NGỮ CẢNH (UI FILE ĐÍNH KÈM)
    # Nếu có biểu đồ được chọn, hiển thị nó lên đầu khung chat
    if target_data:
        meta = target_data["metadata"]
        # Thẻ hiển thị ảnh nổi bật, có viền bo tròn
        st.markdown("<div style='background: white; padding: 12px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; margin-bottom: 15px;'>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2.5])
        with c1:
            st.image(target_data["image"], use_container_width=True) # Hiển thị ảnh thumbnail
        with c2:
            st.markdown(f"**📎 Biểu đồ đính kèm**")
            # Hiển thị thông tin trục X, Y của biểu đồ để người dùng nắm bối cảnh
            if meta.get("x_label") and meta.get("y_label"):
                st.markdown(f"<span style='color:#64748B; font-size:13px;'>Trục Y: {meta['y_label']}<br>Trục X: {meta['x_label']}</span>", unsafe_allow_html=True)
            
            # Nút gỡ ảnh gọn gàng (hủy chọn biểu đồ)
            if st.button("✖ Gỡ ảnh", key="remove_img", use_container_width=False):
                st.session_state.AI_VISION_TARGET = None
                st.rerun(scope="fragment") # Chỉ tải lại vùng fragment này
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Nhắc nhở nếu chưa có biểu đồ nào được đính kèm
        st.info("💡 Chưa có biểu đồ nào. Hãy chọn 'Phân tích' dưới một biểu đồ để bắt đầu.")

    # 2. KHUNG HIỂN THỊ TIN NHẮN
    chat_box = st.container(height=450)
    with chat_box:
        # Màn hình chào mừng nếu chưa có tin nhắn nào trong lịch sử
        if not st.session_state.CHAT_HISTORY:
            st.markdown("""
                <div style="text-align: center; color: #94A3B8; padding-top: 50px;">
                    <h3 style="color: #64748B;">👋 Xin chào!</h3>
                    <p>Tôi là trợ lý AI chuyên phân tích số liệu.<br>Bạn muốn hỏi gì về biểu đồ này?</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Lặp qua và hiển thị toàn bộ tin nhắn trước đó
            for msg in st.session_state.CHAT_HISTORY:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    # 3. THANH NHẬP LIỆU (NATIVE CHAT INPUT CỦA STREAMLIT)
    # Khung nhập câu hỏi ở dưới cùng
    if u_msg := st.chat_input("Hỏi AI (VD: Nhận xét xu hướng điểm số...)", key="chat_input"):
        # Chặn không cho hỏi nếu chưa đính kèm ảnh
        if not target_data:
            st.warning("Vui lòng đính kèm một biểu đồ trước khi hỏi.")
            st.rerun(scope="fragment")
            
        # Lưu tin nhắn người dùng vào lịch sử và hiển thị lên màn hình
        st.session_state.CHAT_HISTORY.append({"role": "user", "content": u_msg})
        with chat_box:
            with st.chat_message("user"): 
                st.markdown(u_msg)
            
            # Khối xử lý của AI Assistant
            with st.chat_message("assistant"):
                with st.spinner("AI đang phân tích biểu đồ..."):
                    try:
                        # Ghép prompt hệ thống, thông tin biểu đồ và câu hỏi của người dùng
                        sys_prompt = load_system_prompt()
                        meta = target_data["metadata"]
                        
                        full_prompt = f"""
                        {sys_prompt}
                        
                        DỮ LIỆU ĐANG XEM:
                        - Biểu đồ đo lường: {meta.get('y_label', 'Không rõ')}
                        - Phân loại theo: {meta.get('x_label', 'Không rõ')}
                        
                        CÂU HỎI: {u_msg}
                        """
                        
                        # Gửi yêu cầu tới mô hình Gemini kèm theo hình ảnh biểu đồ
                        res = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[full_prompt, target_data["image"]]
                        )
                        # Hiển thị câu trả lời và lưu vào lịch sử
                        st.markdown(res.text)
                        st.session_state.CHAT_HISTORY.append({"role": "assistant", "content": res.text})
                    except Exception as e:
                        st.error(f"Lỗi kết nối AI: {e}")
        
        st.rerun(scope="fragment")

    # 4. NÚT DỌN DẸP LỊCH SỬ CHAT
    # Chỉ hiện nút xóa khi có tin nhắn trong lịch sử
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
    """Hàm này được gọi từ file main để gắn nút Chatbot vào Sidebar"""
    st.sidebar.markdown("""
        <style>
        /* CSS Nút Popover ngoài Sidebar - Làm cho nút to và nổi bật hơn */
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
            transform: translateY(-2px); /* Hiệu ứng nẩy lên khi hover */
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
        # Nút popover mở ra giao diện chatbot
        with st.popover("✨ Trợ lý AI", use_container_width=True):
            chatbot_inner_logic()