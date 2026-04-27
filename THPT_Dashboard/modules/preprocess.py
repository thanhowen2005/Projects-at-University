import pandas as pd
import numpy as np

def add_province(df, df_mavung):
    """Trích xuất 2 số đầu sbd và merge với tên tỉnh"""
    if df.empty or df_mavung.empty:
        return df
        
    # Đảm bảo sbd có 8 ký tự, lấy 2 ký tự đầu
    df['Ma'] = df['sbd'].astype(str).str.zfill(8).str[:2]
    df_mavung['Ma'] = df_mavung['Ma'].astype(str).str.zfill(2)
    
    # Merge để lấy tên tỉnh
    df = df.merge(df_mavung, on='Ma', how='left')
    return df


import pandas as pd

def add_khoi_thi(df):
    if df.empty:
        return df

    # Đếm số môn trong từng tổ hợp
    natural = df[['vat_ly','hoa_hoc','sinh_hoc']].notna().sum(axis=1)
    social = df[['lich_su','dia_ly','gdcd']].notna().sum(axis=1)

    # Khởi tạo cột
    df['khoi_thi'] = 'Thi không đầy đủ tổ hợp'

    # 1. KHTN: đủ 3 môn tự nhiên, không có xã hội
    df.loc[(natural == 3) & (social == 0), 'khoi_thi'] = 'KHTN'

    # 2. KHXH: đủ 3 môn xã hội, không có tự nhiên
    df.loc[(social == 3) & (natural == 0), 'khoi_thi'] = 'KHXH'

    return df

def get_subject_means(df):
    """Tính điểm trung bình của tất cả các môn học"""
    subjects = ['toan', 'ngu_van', 'ngoai_ngu', 'vat_ly', 'hoa_hoc', 'sinh_hoc', 'lich_su', 'dia_ly', 'gdcd']
    
    # Lọc các môn thực sự có trong dataframe
    existing_subjects = [sub for sub in subjects if sub in df.columns]
    
    # Tính mean, reset index để vẽ biểu đồ
    means = df[existing_subjects].mean().reset_index()
    means.columns = ['Môn thi', 'Điểm trung bình']
    
    # Map tên môn
    subject_map = {
        'toan': 'Toán', 'ngu_van': 'Ngữ Văn', 'ngoai_ngu': 'Ngoại Ngữ',
        'vat_ly': 'Vật Lý', 'hoa_hoc': 'Hóa Học', 'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử', 'dia_ly': 'Địa Lý', 'gdcd': 'GDCD'
    }
    means['Môn thi'] = means['Môn thi'].map(subject_map)
    return means