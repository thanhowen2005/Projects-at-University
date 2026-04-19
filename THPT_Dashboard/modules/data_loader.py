import pandas as pd
import streamlit as st
import glob
import os
import re

@st.cache_data
def load_data(data_dir="data/processed"):
    """
    Load và concat tất cả các file thpt*.csv trong thư mục data, 
    đồng thời load file mavung.csv
    """
    df_list = []
    
    # Tìm tất cả các file có định dạng thptYYYY.csv
    file_pattern = os.path.join(data_dir, "thpt*.csv")
    files = glob.glob(file_pattern)
    
    if not files:
        st.error(f"⚠️ Không tìm thấy file dữ liệu nào tại {data_dir}/thpt*.csv")
        return pd.DataFrame(), pd.DataFrame()
        
    for file_path in files:
        # Extract năm từ tên file bằng regex
        match = re.search(r'thpt(\d{4})\.csv', file_path)
        if match:
            year = int(match.group(1))
            # Ép kiểu sbd thành chuỗi để không mất số 0 ở đầu
            df_year = pd.read_csv(file_path, dtype={'sbd': str})
            df_year['nam'] = year
            df_list.append(df_year)
            
    # Concat data các năm
    df_scores = pd.concat(df_list, ignore_index=True)
    
    # Load mã vùng
    mavung_path = os.path.join(data_dir, "mavung.csv")
    if os.path.exists(mavung_path):
        df_mavung = pd.read_csv(mavung_path, dtype={'Ma': str})
    else:
        st.warning(f"⚠️ Không tìm thấy file {mavung_path}")
        df_mavung = pd.DataFrame(columns=['Ma', 'Ten Tinh'])
        
    return df_scores, df_mavung