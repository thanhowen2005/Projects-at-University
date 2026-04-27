import pandas as pd
import streamlit as st
import glob
import os
import re

NEEDED_COLS = [
    'sbd', 'toan', 'ngu_van', 'ngoai_ngu', 
    'vat_ly', 'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd'
]

# Ép kiểu dữ liệu
DTYPE_SETTINGS = {
    'sbd': str,          # Giữ số 0 ở đầu
    'toan': 'float32',   
    'ngu_van': 'float32',
    'ngoai_ngu': 'float32',
    'vat_ly': 'float32',
    'hoa_hoc': 'float32',
    'sinh_hoc': 'float32',
    'lich_su': 'float32',
    'dia_ly': 'float32',
    'gdcd': 'float32'
}

@st.cache_data(max_entries=1)
def load_data(data_dir="data/processed"):
    """
    Load và concat tất cả các file thpt*.csv với cơ chế ÉP KIỂU ĐỂ GIẢM RAM, 
    đồng thời load file mavung.csv
    """
    df_list = []
    
    file_pattern = os.path.join(data_dir, "thpt*.csv")
    files = glob.glob(file_pattern)
    
    if not files:
        st.error(f"⚠️ Không tìm thấy file dữ liệu nào tại {data_dir}/thpt*.csv")
        return pd.DataFrame(), pd.DataFrame()
        
    for file_path in files:
        match = re.search(r'thpt(\d{4})\.csv', file_path)
        if match:
            year = int(match.group(1))
            
            # Lọc các cột có trong NEEDED_COLS mà file CSV thực sự có 
            cols_in_file = pd.read_csv(file_path, nrows=0).columns
            use_cols = [c for c in NEEDED_COLS if c in cols_in_file]
            
            df_year = pd.read_csv(
                file_path, 
                usecols=use_cols, 
                dtype=DTYPE_SETTINGS
            )
            
            # Ép kiểu int16 cho cột năm
            df_year['nam'] = year
            df_year['nam'] = df_year['nam'].astype('int16') 
            
            df_list.append(df_year)
            
    # Concat data các năm
    df_scores = pd.concat(df_list, ignore_index=True)
    
    # Load mã vùng
    mavung_path = os.path.join(data_dir, "mavung.csv")
    if os.path.exists(mavung_path):
        df_mavung = pd.read_csv(mavung_path, dtype={'Ma': str})
        # Biến cột 'Ten Tinh' thành dạng category để tối ưu hóa nếu cần merge sau này
        if 'Ten Tinh' in df_mavung.columns:
            df_mavung['Ten Tinh'] = df_mavung['Ten Tinh'].astype('category')
    else:
        st.warning(f"⚠️ Không tìm thấy file {mavung_path}")
        df_mavung = pd.DataFrame(columns=['Ma', 'Ten Tinh'])
        
    return df_scores, df_mavung