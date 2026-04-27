import streamlit as st
import plotly.io as pio
from PIL import Image
import io

@st.fragment # 
def render_isolated_chart(fig, chart_id):
    fig.update_layout(
        margin=dict(l=80, r=40, t=30, b=50),
        yaxis=dict(automargin=True),
        xaxis=dict(automargin=True)
    )

    # CSS Nút bấm (Xanh đậm, chữ trắng)
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

    st.plotly_chart_original(fig, use_container_width=True)
    
    if st.button(f"✨ Phân tích biểu đồ với trợ lý AI", key=f"btn_{chart_id}"):
        # --- LẤY TRỰC TIẾP TỪ TITLE TRỤC ---
        meta = {
            "x_label": fig.layout.xaxis.title.text or "",
            "y_label": fig.layout.yaxis.title.text or ""
        }
        
        # Chụp ảnh tĩnh (scale=2 để AI nhìn rõ số liệu)
        img_bytes = pio.to_image(fig, format='png', scale=2)
        
        st.session_state.AI_VISION_TARGET = {
            "image": Image.open(io.BytesIO(img_bytes)),
            "metadata": meta
        }
        st.toast(f"Đã thêm biểu đồ vào trợ lý AI", icon="✅")

# --- CƠ CHẾ ĐÁNH TRÁO HÀM ---
if not hasattr(st, 'plotly_chart_original'):
    st.plotly_chart_original = st.plotly_chart

def patched_plotly_chart(fig, **kwargs):
    if 'chart_counter' not in st.session_state:
        st.session_state.chart_counter = 0
    st.session_state.chart_counter += 1
    render_isolated_chart(fig, chart_id=f"auto_{st.session_state.chart_counter}")

st.plotly_chart = patched_plotly_chart