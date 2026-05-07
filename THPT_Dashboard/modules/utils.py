import streamlit as st
import plotly.io as pio
from PIL import Image
import io

# Tách biệt scope render. Nút bấm trong này không làm reload toàn bộ app.
@st.fragment 
def render_isolated_chart(fig, chart_id):
    # Auto-margin để tránh nhãn trục X, Y bị cắt lẹm
    fig.update_layout(
        margin=dict(l=80, r=40, t=30, b=50),
        yaxis=dict(automargin=True),
        xaxis=dict(automargin=True)
    )

    st.markdown(f"""
        <style>
        div.stButton > button[key*="btn_{chart_id}"] {{
            background-color: #14357A !important;
            color: white !important;
            border: 1px solid #6FA8DC !important;
            border-radius: 8px !important;
            width: 100% !important;
            height: 38px !important;
        }}
        div.stButton > button[key*="btn_{chart_id}"] p {{ color: white !important; font-weight: 500 !important; }}
        </style>
    """, unsafe_allow_html=True)

    # Render biểu đồ bằng hàm gốc
    st.plotly_chart_original(fig, use_container_width=True)
    
    # Nút trigger tính năng AI Vision
    if st.button(f"✨ Phân tích biểu đồ với trợ lý AI", key=f"btn_{chart_id}"):
        # Lấy label trục tọa độ làm metadata ngữ cảnh cho AI
        meta = {
            "x_label": fig.layout.xaxis.title.text or "",
            "y_label": fig.layout.yaxis.title.text or ""
        }
        
        # Export Plotly fig sang byte ảnh PNG (scale=2 để tăng độ phân giải)
        img_bytes = pio.to_image(fig, format='png', scale=2)
        
        # Đẩy payload (ảnh + metadata) vào Session State để Popover Chatbot bắt lấy
        st.session_state.AI_VISION_TARGET = {
            "image": Image.open(io.BytesIO(img_bytes)),
            "metadata": meta
        }
        st.toast(f"Đã thêm biểu đồ vào trợ lý AI", icon="✅")

# ==========================================
# MONKEY PATCHING: GHI ĐÈ HÀM PLOTLY CỦA STREAMLIT
# ==========================================
# 1. Backup hàm render mặc định
if not hasattr(st, 'plotly_chart_original'):
    st.plotly_chart_original = st.plotly_chart

# 2. Định nghĩa hàm bọc (wrapper function)
def patched_plotly_chart(fig, **kwargs):
    # Cấp phát ID duy nhất cho mỗi biểu đồ được render
    if 'chart_counter' not in st.session_state:
        st.session_state.chart_counter = 0
    st.session_state.chart_counter += 1
    
    # Render UI đã được custom (Chart + Nút AI)
    render_isolated_chart(fig, chart_id=f"auto_{st.session_state.chart_counter}")

# 3. Tráo đổi hàm: Thay st.plotly_chart bằng hàm wrapper
st.plotly_chart = patched_plotly_chart