# Tab 4: Phân tích Khối thi & Xét tuyển (Academic Blocks)

## 1. Phổ điểm tổng cộng của khối thi trong năm được chọn là gì?

### What (Data):
- Tổng điểm 3 môn: Định lượng (Quantitative) - Dữ liệu dẫn xuất (Ví dụ: A00 = Toán + Lý + Hóa).
- Số lượng thí sinh: Định lượng (Count SBD).
- Bộ lọc: Khối thi và Năm.

### Why (Task):
Analyze Distribution. Giúp xác định chính xác độ "loãng" hay "đặc" của điểm số trong một năm cụ thể. Thí sinh dựa vào đây để biết mình đang nằm ở đâu trong tổng thể những người cùng thi khối đó.

### How (Visual):
Histogram.

### Biện luận:
Histogram với các cột sát nhau cho phép soi rõ sự biến động ở từng ngưỡng điểm nhỏ (ví dụ: bin size = 0.5 hoặc 1 điểm). Đây là căn cứ quan trọng nhất để dự báo điểm chuẩn của các trường Đại học.


## 2. Xu hướng ngưỡng điểm "Top 10%" của mỗi khối thi biến động ra sao qua 5 năm?

### What (Data):
- Năm: Thứ tự (Ordered) từ 2021 - 2025.
- Ngưỡng điểm Percentile 90 (Top 10%): Định lượng.
- Khối thi: Phân loại (Categorical).

### Why (Task):
Identify Trend & Compare. Trả lời câu hỏi: "Để lọt vào nhóm 10% giỏi nhất khối A00 năm 2025 cần bao nhiêu điểm so với các năm trước?". Điều này giúp nhận diện hiện tượng lạm phát điểm số ở nhóm các trường Đại học Top đầu.

### How (Visual):
Line Chart (Biểu đồ đường).

### Biện luận:
Biểu đồ đường là lựa chọn tối ưu nhất để theo dõi sự thay đổi liên tục qua thời gian. Việc vẽ nhiều đường (mỗi đường một khối thi) trên cùng một trục giúp so sánh trực quan mức độ khốc liệt giữa các khối qua từng năm.


## 3. Điểm trung bình của từng môn thành phần trong khối thi là bao nhiêu?

### What (Data):
- Tên môn học trong khối: Định danh (Categorical). Ví dụ: Khối D01 gồm Toán, Văn, Anh.
- Điểm trung bình môn: Định lượng (Quantitative).
- Bộ lọc: Khối thi và Năm.

### Why (Task):
Component Analysis (Phân tích thành phần). Giải thích cho kết quả ở Câu 1: Tại sao tổng điểm khối năm nay lại cao/thấp? Do môn nào "gánh" điểm và môn nào "kéo" điểm của cả khối đi xuống?

### How (Visual):
Radar Chart (Biểu đồ mạng nhện) hoặc Column Chart.

### Biện luận:
Biểu đồ mạng nhện thể hiện rõ sự cân bằng năng lực. Nếu màng nhện bị kéo lệch về một đỉnh, đó là môn thế mạnh của thí sinh khối đó trong năm đó. Nếu dùng cột, sự chênh lệch độ cao giữa 3 môn sẽ cho cái nhìn trực diện về độ khó của đề thi từng môn.


# Tổng kết Tab 4

Tab 4 tập trung vào phân tích khối thi và góc nhìn xét tuyển đại học, giúp người dùng:

- Hiểu phân phối điểm tổng của từng khối trong từng năm
- Theo dõi sự thay đổi của ngưỡng điểm top 10% qua thời gian
- Phân tích đóng góp của từng môn trong tổng điểm khối

Đây là lớp phân tích chuyển từ dữ liệu môn học đơn lẻ sang cấu trúc tổ hợp xét tuyển, giúp đánh giá trực tiếp độ khó và tính cạnh tranh của từng khối thi trong hệ thống tuyển sinh đại học.