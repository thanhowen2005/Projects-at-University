import streamlit as st
import pandas as pd
import numpy as np
import pickle
from scipy.special import inv_boxcox
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import plotly.express as px  # Thư viện vẽ biểu đồ tương tác

# Style cho matplotlib/seaborn (dùng cho Tab 2)
plt.style.use("seaborn-v0_8-darkgrid")

# =========================
# 1. PAGE CONFIGURATION
# =========================
st.set_page_config(page_title="Big Mart Predictor", page_icon="🛒", layout="wide")

# =========================
# 2. LOAD (CACHED)
# =========================
@st.cache_resource
def load_model():
    model = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/model.pkl", "rb"))
    scaler = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/scaler.pkl", "rb"))
    lambda_ = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/lambda.pkl", "rb"))
    columns = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/columns.pkl", "rb"))
    return model, scaler, lambda_, columns

@st.cache_data
def load_data():
    # 1. Đọc trực tiếp 2 file đã clean (gồm cả đặc trưng và biến mục tiêu)
    train_df = pd.read_csv("BigMart_Sales_Analysis/data/train_data/train.csv")
    test_df = pd.read_csv("BigMart_Sales_Analysis/data/test_data/test.csv")

    # 2. Gộp Train và Test thành một DataFrame hoàn chỉnh để vẽ biểu đồ
    df = pd.concat([train_df, test_df], ignore_index=True)

    # 3. Load y_test và y_pred để vẽ phần Đánh giá mô hình (Tab 2)
    y_test_eval = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/y_test.pkl", "rb"))
    y_pred_eval = pickle.load(open("BigMart_Sales_Analysis/Model/saved_model/y_pred.pkl", "rb"))
    
    y_test_eval = np.array(y_test_eval).ravel()
    y_pred_eval = np.array(y_pred_eval).ravel()

    return df, y_test_eval, y_pred_eval

# Load dữ liệu ngầm
try:
    model, scaler, lambda_, columns = load_model()
    df, y_test, y_pred = load_data()
except Exception as e:
    st.error("⚠️ Lỗi tải dữ liệu. Vui lòng kiểm tra lại thư mục model/ và data/")
    st.stop()

# =========================
# 3. HEADER
# =========================
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>🛒 Big Mart Sales Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555; font-size: 1.2rem;'>Ứng dụng dự báo doanh số bán lẻ (Linear Regression & Power-BoxCox)</p>", unsafe_allow_html=True)
st.markdown("---")

# =========================
# 4. SIDEBAR INPUT
# =========================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3081/3081840.png", width=80)
st.sidebar.markdown("## ⚙️ Thông số đầu vào")

def create_number_input(col_name, label, step, fmt="%.2f"):
    return st.sidebar.number_input(
        label,
        min_value=float(df[col_name].min()) if col_name in df.columns else 0.0,
        max_value=float(df[col_name].max()) if col_name in df.columns else 1000.0,
        value=float(df[col_name].mean()) if col_name in df.columns else 0.0,
        step=step,
        format=fmt
    )

# --- Group 1: Product Details ---
with st.sidebar.expander("📦 THÔNG TIN SẢN PHẨM", expanded=True):
    item_mrp = create_number_input("Item_MRP", "Giá niêm yết (Item MRP - $)", 0.01)
    item_type = st.selectbox(
        "Loại sản phẩm (Item Type)",
        ["Dairy", "Soft Drinks", "Meat", "Fruits and Vegetables",
         "Household", "Baking Goods", "Snack Foods", "Frozen Foods",
         "Breakfast", "Health and Hygiene", "Hard Drinks", "Canned",
         "Breads", "Starchy Foods", "Others", "Seafood"]
    )
    item_fat = st.selectbox("Độ béo (Item Fat Content)", ["Low Fat", "Regular", "Non-Edible"])
    item_weight = create_number_input("Item_Weight", "Trọng lượng (Item Weight)", 0.01)
    item_visibility = create_number_input("Item_Visibility", "Độ hiển thị (Item Visibility)", 0.0001, "%.4f")

# --- Group 2: Store Details ---
with st.sidebar.expander("🏪 THÔNG TIN CỬA HÀNG", expanded=True):
    outlet_type = st.selectbox(
        "Loại cửa hàng (Outlet Type)",
        ["Supermarket Type3", "Supermarket Type1", "Supermarket Type2", "Grocery Store"]
    )
    outlet_location = st.selectbox("Vị trí (Outlet Location)", ["Tier 1", "Tier 2", "Tier 3"])
    outlet_size = st.selectbox("Quy mô (Outlet Size)", ["Small", "Medium", "High"])
    
    outlet_est_year = st.number_input(
        "Năm thành lập (Establishment Year)",
        min_value=1985, max_value=2026, value=1999, step=1
    )

current_year = 2026
outlet_years = current_year - outlet_est_year

# =========================
# 5. PREPROCESS INPUT CHO MÔ HÌNH
# =========================
size_map = {"Small": 0, "Medium": 1, "High": 2}
loc_map = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}

input_df = pd.DataFrame(columns=columns)
input_df.loc[0] = 0

input_df["Item_Weight"] = item_weight
input_df["Item_Visibility"] = item_visibility
input_df["Item_MRP"] = item_mrp
input_df["Outlet_Years"] = outlet_years
input_df["Outlet_Size"] = size_map[outlet_size]
input_df["Outlet_Location_Type"] = loc_map[outlet_location]

def safe_set(col):
    if col in input_df.columns:
        input_df[col] = 1

safe_set(f"Outlet_Type_{outlet_type}")
safe_set(f"Item_Fat_Content_{item_fat}")
safe_set(f"Item_Type_{item_type}")

# Thực hiện scale cho dữ liệu đầu vào
num_cols = ["Item_Weight", "Item_Visibility", "Item_MRP", "Outlet_Years"]
input_df[num_cols] = scaler.transform(input_df[num_cols])

# =========================
# 6. MAIN LAYOUT (TABS)
# =========================
tab1, tab2, tab3 = st.tabs(["🔮 Dự đoán Doanh số (Prediction)", "📊 Đánh giá Mô hình (Analytics)", "🔍 Khám phá Dữ liệu (Discovery)"])

# -------------------------
# TAB 1: PREDICTION
# -------------------------
with tab1:
    col_btn, col_res = st.columns([1, 2])
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            f"**📋 TÓM TẮT THÔNG SỐ ĐẦU VÀO:**\n\n"
            f"**📦 THÔNG TIN SẢN PHẨM**\n"
            f"- **Loại sản phẩm:** {item_type}\n"
            f"- **Độ béo:** {item_fat}\n"
            f"- **Giá niêm yết:** ${item_mrp:,.2f}\n"
            f"- **Trọng lượng:** {item_weight:.2f}\n"
            f"- **Độ hiển thị:** {item_visibility:.4f}\n\n"
            f"**🏪 THÔNG TIN CỬA HÀNG**\n"
            f"- **Loại cửa hàng:** {outlet_type}\n"
            f"- **Vị trí:** {outlet_location}\n"
            f"- **Quy mô:** {outlet_size}\n"
            f"- **Năm thành lập:** {outlet_est_year} (Tuổi đời: {outlet_years} năm)"
        )
        predict_btn = st.button("🚀 THỰC HIỆN DỰ ĐOÁN", use_container_width=True, type="primary")

    with col_res:
        if predict_btn:
            pred_bc = model.predict(input_df)
            pred = inv_boxcox(pred_bc, lambda_) - 1
            user_pred = pred[0]

            st.markdown(
                f"""
                <div style="background-color: #D4EDDA; padding: 20px; border-radius: 10px; border: 2px solid #28A745; text-align: center;">
                    <h3 style="color: #155724; margin: 0;">DOANH SỐ DỰ KIẾN (USD)</h3>
                    <h1 style="color: #28A745; font-size: 3.5rem; margin: 0;">${user_pred:,.2f}</h1>
                </div>
                """, 
                unsafe_allow_html=True
            )
            st.balloons()
        else:
            st.markdown(
                """
                <div style="background-color: #F8F9FA; padding: 20px; border-radius: 10px; border: 2px dashed #CED4DA; text-align: center;">
                    <h4 style="color: #6C757D;">Chờ lệnh dự đoán...</h4>
                    <p style="color: #6C757D;">Nhấn nút "Thực hiện dự đoán" để xem kết quả.</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

# -------------------------
# TAB 2: METRICS & DIAGNOSTICS
# -------------------------
with tab2:
    def compute_metrics(y_test, y_pred):
        min_len = min(len(y_test), len(y_pred))
        y_test_sub = y_test[:min_len]
        y_pred_sub = y_pred[:min_len]

        mae = mean_absolute_error(y_test_sub, y_pred_sub)
        mse = mean_squared_error(y_test_sub, y_pred_sub)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test_sub, y_pred_sub)
        return mae, mse, rmse, r2

    mae, mse, rmse, r2 = compute_metrics(y_test, y_pred)

    st.subheader("🎯 Hiệu suất Mô hình (Test Set)")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("R² Score (Độ khớp)", f"{r2:.4f}", help="Càng gần 1 càng tốt")
    m2.metric("RMSE (Sai số trung bình)", f"${rmse:,.2f}", help="Càng thấp càng tốt")
    m3.metric("MAE", f"${mae:,.2f}")
    m4.metric("MSE", f"{mse:,.0f}")
    
    st.markdown("---")
    st.subheader("📈 Diagnostic Plots (Kiểm tra phân phối lỗi)")
    
    def plot_model(y_test, y_pred):
        residuals = y_test - y_pred
        min_val = min(y_test.min(), y_pred.min())
        max_val = max(y_test.max(), y_pred.max())

        fig, ax = plt.subplots(1, 3, figsize=(18, 5))
        fig.patch.set_facecolor('#F8F9FA')

        # 1. Pred vs Actual
        sns.scatterplot(x=y_test, y=y_pred, color='#20B2AA', alpha=0.5, edgecolor=None, ax=ax[0])
        ax[0].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2)
        ax[0].set_title("Predicted vs Actual", fontweight='bold')
        ax[0].set_xlabel("Actual Sales")
        ax[0].set_ylabel("Predicted Sales")

        # 2. Residual
        sns.scatterplot(x=y_pred, y=residuals, color='#FF8C00', alpha=0.5, edgecolor=None, ax=ax[1])
        ax[1].axhline(0, color='red', linestyle='--', linewidth=2)
        ax[1].set_title("Residual Plot (Homoscedasticity)", fontweight='bold')
        ax[1].set_xlabel("Predicted Sales")
        ax[1].set_ylabel("Residuals")

        # 3. Histogram
        sns.histplot(residuals, bins=40, color='#8A2BE2', alpha=0.7, kde=True, ax=ax[2])
        ax[2].set_title("Error Distribution (Normality)", fontweight='bold')
        ax[2].set_xlabel("Residual Value")

        plt.tight_layout()
        st.pyplot(fig)

    with st.spinner("Đang vẽ biểu đồ..."):
        plot_model(y_test, y_pred)

    # === FEATURE IMPORTANCE ===
    st.markdown("---")
    st.subheader("🌟 Mức độ quan trọng của đặc trưng (Feature Importance)")
    st.caption("Biểu đồ thể hiện các yếu tố tác động mạnh nhất đến dự đoán của mô hình Linear Regression.")
    
    try:
        coefs = model.coef_
        importance_df = pd.DataFrame({
            'Feature': columns,
            'Coefficient': coefs.flatten()
        })
        importance_df['Abs_Impact'] = importance_df['Coefficient'].abs()
        top_10_features = importance_df.sort_values(by='Abs_Impact', ascending=True).tail(10)

        fig_imp = px.bar(
            top_10_features, 
            x='Coefficient', 
            y='Feature', 
            orientation='h',
            color='Coefficient', 
            color_continuous_scale=px.colors.diverging.RdBu,
            title="Top 10 Yếu tố tác động đến Doanh thu"
        )
        fig_imp.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_imp, use_container_width=True)
    except Exception as e:
        st.info("Mô hình không hỗ trợ trích xuất thuộc tính coef_ để vẽ Feature Importance.")

# -------------------------
# TAB 3: DATA DISCOVERY (ALL FEATURES)
# -------------------------
with tab3:
    st.subheader("🔍 Tương quan giữa TẤT CẢ Đặc trưng và Doanh thu")
    st.markdown("Khám phá chi tiết cách từng biến số học và biến phân loại tác động đến Doanh thu (Item Outlet Sales).")

    target_col = "Item_Outlet_Sales"
    num_cols_plot = ["Item_Weight", "Item_Visibility", "Item_MRP", "Outlet_Years"]
    cat_cols_plot = ["Item_Fat_Content", "Outlet_Size", "Outlet_Location_Type", "Outlet_Type"] 

    # --- 1. MA TRẬN TƯƠNG QUAN TỔNG THỂ ---
    st.markdown("#### 1. Ma trận tương quan (Numerical Features)")
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    fig_corr = px.imshow(
        corr_matrix, 
        text_auto=".2f", 
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")

    # --- 2. BIẾN SỐ HỌC (NUMERICAL) VS TARGET ---
    st.markdown("#### 2. Biến Số học (Numerical) vs Doanh thu")
    st.caption("Biểu đồ phân tán (Scatter Plot) giúp phát hiện xu hướng tuyến tính hoặc các điểm bất thường.")
    
    cols_num = st.columns(2)
    for i, col in enumerate(num_cols_plot):
        if col in df.columns:
            fig_scatter = px.scatter(
                df, x=col, y=target_col, 
                opacity=0.4, color_discrete_sequence=['#2E86C1'],
                title=f"{col} vs {target_col}"
            )
            cols_num[i % 2].plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # --- 3. BIẾN PHÂN LOẠI (CATEGORICAL) VS TARGET ---
    st.markdown("#### 3. Biến Phân loại (Categorical) vs Doanh thu")
    st.caption("Biểu đồ hộp (Boxplot) giúp so sánh mức phân phối, giá trị trung vị và các khoảng outlier giữa các nhóm.")
    
    cols_cat = st.columns(2)
    for i, col in enumerate(cat_cols_plot):
        if col in df.columns:
            fig_box = px.box(
                df, x=col, y=target_col, 
                color=col,
                title=f"{col} vs {target_col}"
            )
            fig_box.update_layout(showlegend=False)
            cols_cat[i % 2].plotly_chart(fig_box, use_container_width=True)

    # Vẽ riêng Item_Type full width
    if "Item_Type" in df.columns:
        st.markdown("<br>", unsafe_allow_html=True)
        fig_item_type = px.box(
            df, x="Item_Type", y=target_col, 
            color="Item_Type",
            title="Item_Type vs Item_Outlet_Sales (Chi tiết danh mục sản phẩm)"
        )
        fig_item_type.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_item_type, use_container_width=True)

# =========================
# 7. FOOTER
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Retail Analytics Dashboard. Developed using Streamlit, Scikit-Learn & Plotly.")