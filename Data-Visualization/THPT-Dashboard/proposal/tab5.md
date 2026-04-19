# Tab 5: Phân tích Chuyên sâu & Xu hướng (Insights)


## 1. Môn học nào có mức độ khó ổn định nhất qua các năm?

### What (Data):
- Điểm trung bình (Quantitative) của tất cả các môn qua từng năm.

### Why (Task):
Consistency Analysis. Xác định môn học nào có "phong độ" ra đề ổn định nhất, giúp thí sinh có kế hoạch ôn tập an tâm hơn.

### How (Visual):
Small Multiples Line Charts (Các biểu đồ đường nhỏ đặt cạnh nhau).

### Biện luận:
Việc đặt các biểu đồ nhỏ giúp bạn thấy ngay môn nào có đường biểu diễn "phẳng" nhất (ít biến động) và môn nào "nhảy múa" thất thường (biến động mạnh).


## 2. Khối thi nào có tổng điểm ít biến động nhất qua thời gian?

### What (Data):
- Tổng điểm trung bình của các khối thi (A00, B00, C00, D01, A01) qua các năm.

### Why (Task):
Predictability Analysis. Giúp thí sinh dự đoán điểm chuẩn chính xác hơn. Những khối thi ổn định sẽ có điểm chuẩn ít gây "sốc" hơn so với các khối có điểm số biến động mạnh.

### How (Visual):
Multi-series Line Chart (Biểu đồ đường nhiều nhánh).

### Biện luận:
Vẽ các đường kẻ cho mỗi khối trên cùng một trục tọa độ. Khối nào có đường nằm ngang nhất chính là khối ổn định nhất về mặt điểm số.


## 3. Đối đầu Hà Nội vs. TP.HCM: Sự khác biệt về năng lực ở 3 môn xương sống (Toán, Văn, Anh)?

### What (Data):
- Địa phương: Hà Nội và TP.HCM (Categorical).
- Môn học: Toán, Ngữ văn, Ngoại ngữ.
- Chỉ số: Điểm trung bình (Average) và Tỷ lệ điểm giỏi ≥ 8.0.

### Why (Task):
Head-to-Head Comparison. So sánh trực diện năng lực đào tạo ở 3 môn cốt lõi giữa hai trung tâm giáo dục lớn nhất cả nước. Điều này giúp kiểm chứng thực tế: "Liệu TP.HCM có thực sự áp đảo về Ngoại ngữ và Hà Nội có mạnh hơn về Toán/Văn?".

### How (Visual):
Dumbbell Chart (Biểu đồ tạ đơn) hoặc Grouped Bar Chart.

### Biện luận:
Với Dumbbell Chart, mỗi "thanh tạ" đại diện cho một môn học. Hai đầu quả tạ là Hà Nội và TP.HCM. Khoảng cách giữa hai đầu quả tạ chính là "khoảng cách năng lực" ở môn đó. Đây là cách so sánh đối đầu trực quan và mạnh mẽ nhất.

## 4. Tổ hợp nào đang có sự lệch pha giữa mức độ phổ biến và hiệu suất điểm số?

### What (Data)
- Tổ hợp thi (Categorical)
- Tỷ lệ thí sinh lựa chọn tổ hợp (Quantitative)
- Điểm trung bình tổng tổ hợp hoặc điểm trung bình 3 môn thành phần (Quantitative)
- Bộ lọc: Năm

### Why (Task)
- **Compare**: Đối chiếu giữa "độ hot" và chất lượng đầu ra của từng tổ hợp  
- **Identify Outliers**: Phát hiện các tổ hợp được chọn nhiều nhưng hiệu suất không cao, hoặc ngược lại  

Mục tiêu là giúp người dùng trả lời một câu hỏi thực tế hơn: liệu thí sinh đang chọn tổ hợp vì xu hướng, vì định hướng ngành học, hay vì đó thực sự là tổ hợp có lợi thế về điểm số?

### How (Visual)
- **Scatter Plot / Bubble Chart (Biểu đồ phân tán)**

### Biện luận
Biểu đồ phân tán rất phù hợp để thể hiện hai biến định lượng cùng lúc: một trục là mức độ phổ biến, trục còn lại là hiệu suất điểm số. Cách thể hiện này giúp phát hiện nhanh các vùng đáng chú ý:
- Tổ hợp phổ biến và điểm cao: nhóm "an toàn - hấp dẫn"
- Tổ hợp phổ biến nhưng điểm thấp: nhóm "cạnh tranh/rủi ro"
- Tổ hợp ít người chọn nhưng điểm tốt: nhóm "tiềm năng bị bỏ quên"


# Tổng kết Tab 5

Tab 5 tập trung vào phân tích chuyên sâu và xu hướng dài hạn, giúp tổng hợp các insight quan trọng nhất từ toàn bộ dữ liệu. Các phân tích trong tab này làm rõ mức độ ổn định của môn học và khối thi, đồng thời cung cấp góc nhìn so sánh trực diện giữa hai trung tâm giáo dục lớn nhất cả nước là Hà Nội và TP.HCM. Đây là lớp phân tích cao nhất, đóng vai trò rút ra kết luận chiến lược từ toàn bộ hệ thống dữ liệu.