# 🎓 Hệ thống Phân tích Điểm thi THPT Quốc gia (2020-2024)

Một ứng dụng web tương tác được xây dựng bằng **Streamlit** để phân tích và hiển thị dữ liệu điểm thi THPT Quốc gia từ năm 2020 đến 2024. Ứng dụng cung cấp các công cụ phân tích toàn diện, hình ảnh hóa dữ liệu, và tích hợp chatbot AI để trả lời câu hỏi về dữ liệu.

## ✨ Tính Năng Chính

- 📊 **Toàn Cảnh Kỳ Thi** - Tổng quan về kỳ thi, số lượng thí sinh, và thống kê cơ bản
- 📈 **Chi Tiết Môn Học** - Phân tích điểm số từng môn học với biểu đồ phân bố
- 🎓 **Tổ Hợp Xét Tuyển** - Thống kê các tổ hợp môn học phổ biến
- 🗺️ **Phân Tích Địa Lý** - Bản đồ hiển thị kết quả thi theo địa lý (tỉnh/thành phố)
- 💡 **Tương Quan & Phân Hóa** - Phân tích mối tương quan giữa các môn học
- 🤖 **Chatbot AI** - Trợ lý ảo tích hợp sẵn giúp trả lời câu hỏi về dữ liệu

## 📋 Yêu Cầu Hệ Thống

- Python 3.8 hoặc cao hơn
- pip hoặc conda
- Các thư viện phụ thuộc (xem file `requirements.txt`)

## 🚀 Cài Đặt & Chạy Ứng Dụng

### 1. Giải nén và truy cập thư mục dự án
Tải thư mục bài nộp về máy tính và tiến hành giải nén. Sau đó, mở Terminal (trên macOS/Linux) hoặc Command Prompt/PowerShell (trên Windows) và di chuyển vào thư mục gốc của dự án:

```bash
cd PROJECT_FOLDER
```

### 2. Tạo môi trường ảo (tùy chọn nhưng được khuyên)
```bash
# Sử dụng venv
python -m venv venv
source venv/bin/activate  # Trên Linux/Mac
venv\Scripts\activate     # Trên Windows

# Hoặc sử dụng conda
conda create -n thpt-analysis python=3.10
conda activate thpt-analysis
```

### 3. Cài đặt các thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### 4. Cấu hình `GEMINI_API_KEY`

Để sử dụng tính năng Chatbot AI, bạn cần cấu hình API Key từ Google AI Studio.

#### Bước 1: Lấy API Key

Truy cập:

```text
https://aistudio.google.com/app/apikey
```

Đăng nhập tài khoản Google và tạo API Key mới.

---

#### Bước 2: Tạo thư mục `.streamlit`

Tại thư mục gốc của dự án, tạo thư mục:

```text
.streamlit/
```

---

#### Bước 3: Tạo file `secrets.toml`

Trong thư mục `.streamlit`, tạo file:

```text
.streamlit/secrets.toml
```

---

#### Bước 4: Thêm API Key vào file cấu hình

Mở file `secrets.toml` và thêm nội dung sau:

```toml
GEMINI_API_KEY = "MÃ_API_KEY_CỦA_BẠN"
```

Ví dụ:

```toml
GEMINI_API_KEY = "AIzaSyxxxxxxxxxxxxxxxx"
```

---

#### ⚠️ Lưu ý bảo mật

- Không chia sẻ API Key công khai.
- Không commit file `secrets.toml` lên GitHub.
- Nên thêm file `.streamlit/secrets.toml` vào `.gitignore`.


### 4. Chạy ứng dụng Streamlit
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

## 📁 Cấu Trúc Dự Án

```
PROJECT_FOLDER/
├── app.py                          # File chính Streamlit
├── requirements.txt                # Danh sách thư viện cần cài đặt
├── README.md                       # Tệp này
│
├── .streamlit/                     # Cấu hình Streamlit
│   └── secrets.toml                # Chứa GEMINI_API_KEY
│
├── data/                           # Thư mục chứa dữ liệu
│   ├── raw/                        # Dữ liệu thô ban đầu
│   │   ├── thpt2020.csv
│   │   ├── thpt2021.csv
│   │   ├── thpt2022.csv
│   │   ├── thpt2023.csv
│   │   ├── thpt2024.csv
│   │   ├── mavung.csv              # Mã vùng/mã tỉnh
│   │   └── vn_geo.json             # Dữ liệu địa lý Việt Nam
│   │
│   ├── processed/                  # Dữ liệu đã xử lý
│   │   ├── thpt2020.csv
│   │   ├── thpt2021.csv
│   │   ├── thpt2022.csv
│   │   ├── thpt2023.csv
│   │   ├── thpt2024.csv
│   │   ├── mavung.csv
│   │   └── vn_geo.json
│   │
│   ├── eda.ipynb                   # Notebook phân tích dữ liệu
│   └── eda_preprocess.ipynb        # Notebook tiền xử lý
│
├── modules/                        # Các module xử lý chính
│   ├── data_loader.py              # Hàm tải dữ liệu
│   ├── preprocess.py               # Hàm tiền xử lý dữ liệu
│   ├── chatbot.py                  # Tích hợp chatbot AI
│   ├── utils.py                    # Hàm tiện ích
│   └── ai_instruction.txt          # Hướng dẫn cho chatbot AI
│
├── tabs/                           # Các module cho từng tab
│   ├── tab1_overview.py            # Tab: Toàn Cảnh Kỳ Thi
│   ├── tab2_score_dist.py          # Tab: Chi Tiết Môn Học
│   ├── tab3_comb.py                # Tab: Tổ Hợp Xét Tuyển
│   ├── tab4_geo.py                 # Tab: Phân Tích Địa Lý
│   └── tab5_analysis.py            # Tab: Tương Quan & Phân Hóa
│
├── proposal/                       # Thư mục tài liệu proposal
    ├── tab1.md
    ├── tab2.md
    ├── tab3.md
    ├── tab4.md
    └── tab5.md
```

## 📊 Mô Tả Dữ Liệu

### Nguồn Dữ Liệu
- **Thời gian**: 2020-2024
- **Nguồn**: Kỳ thi THPT Quốc gia Việt Nam
- **Các file dữ liệu**:
  - `thpt20XX.csv`: Dữ liệu điểm thi năm 20XX
  - `mavung.csv`: Bảng mã vùng/tỉnh thành phố
  - `vn_geo.json`: Dữ liệu địa lý Việt Nam (GeoJSON)

### Chi Tiết Các Trường Dữ Liệu

1. Các tệp dữ liệu điểm thi (`thpt2020.csv` đến `thpt2024.csv`):
   Chứa các trường thông tin điểm số cơ bản của từng thí sinh:
   - **`sbd`**: Số báo danh của thí sinh (chuỗi 8 ký tự).
   - **`toan`**: Điểm thi bài thi môn Toán.
   - **`ngu_van`**: Điểm thi bài thi môn Ngữ văn.
   - **`ngoai_ngu`**: Điểm thi bài thi môn Ngoại ngữ.
   - **`vat_li`**: Điểm thi bài thi môn Vật lí.
   - **`hoa_hoc`**: Điểm thi bài thi môn Hóa học.
   - **`sinh_hoc`**: Điểm thi bài thi môn Sinh học.
   - **`lich_su`**: Điểm thi bài thi môn Lịch sử.
   - **`dia_li`**: Điểm thi bài thi môn Địa lí.
   - **`gdcd`**: Điểm thi bài thi môn Giáo dục công dân.

2. Tệp tham chiếu địa lý (`mavung.csv`):
   Chứa các trường thông tin dùng để ánh xạ địa lý:
   - **`ma_vung`**: Mã số của hội đồng thi/tỉnh thành (tương ứng với 2 ký tự đầu của Số báo danh).
   - **`ten_tinh`**: Tên tỉnh/thành phố tương ứng với mã vùng.

3. Tệp dữ liệu không gian (`vn_geo.json`):
   Tuân thủ cấu trúc GeoJSON, trong đó phần thuộc tính (`properties`) chứa các trường:
   - **`name`**: Tên tỉnh/thành phố (dùng để liên kết với tệp `mavung.csv`).
   - **`geometry`**: Dữ liệu tọa độ không gian (Polygon hoặc MultiPolygon) dùng để vẽ ranh giới trên bản đồ.

## 🎯 Hướng Dẫn Sử Dụng

### 1. Chọn Tab Phân Tích
Sử dụng menu bên trái để chọn một trong 5 tab phân tích

### 2. Xem Dữ Liệu
Mỗi tab hiển thị các biểu đồ, bảng thống kê và các công cụ lọc dữ liệu

### 3. Sử Dụng Chatbot
- Để thể bắt đầu sử dụng Chatbot, click vào nút "Phân tích biểu đồ với trợ lí AI" nằm ngay bên dưới biểu đồ muốn tìm hiểu
- Nhấp vào phần chatbot ở thanh sidebar
- Đặt câu hỏi về dữ liệu (ví dụ: "Môn nào có điểm cao nhất?")
- Chatbot sẽ phân tích dữ liệu và trả lời

### 4. Tương Tác với Biểu Đồ

- Hover chuột để xem chi tiết
- Click để zoom hoặc chọn/bỏ chọn các phần tử
- Sử dụng các widget để lọc và tùy chỉnh view

## 📦 Thư Viện Chính Sử Dụng

- **Streamlit**: Framework xây dựng giao diện web tương tác cho Dashboard.
- **Pandas**: Nền tảng cốt lõi để đọc, làm sạch và xử lý dữ liệu dạng bảng.
- **Plotly**: Khởi tạo và hiển thị các biểu đồ tương tác chuyên sâu.
- **Pillow (PIL)**: Hỗ trợ xử lý định dạng hình ảnh (sử dụng khi chụp ảnh biểu đồ để nạp vào hệ thống AI).
- **google-genai**: Giao thức kết nối trực tiếp với API của Google Gemini để vận hành tính năng Chatbot AI đa phương thức.

## 🐛 Khắc Phục Sự Cố

### Lỗi: "Không thể tải dữ liệu"
- Kiểm tra xem thư mục `data/processed` có tồn tại không
- Đảm bảo các file CSV có tên chính xác
- Xác nhận file dữ liệu không bị hỏng

### Lỗi: Module không tìm thấy
```bash
pip install -r requirements.txt
```

### Chatbot không hoạt động
- Kiểm tra file `ai_instruction.txt` có tồn tại không
- Xác nhận API key (nếu sử dụng API bên ngoài)
