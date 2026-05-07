# TAB 5: PHÂN TÍCH TƯƠNG QUAN & PHÂN HÓA ĐỀ THI

## 1. Mối quan hệ giữa các môn học trong kỳ thi THPT là gì?

### What (Dữ liệu)
- Điểm số của thí sinh ở 9 môn học chính
- Dữ liệu điểm theo từng năm thi

### Why (Mục tiêu)
- Xác định mức độ liên hệ giữa các môn học trong năng lực học sinh
- Phát hiện các nhóm môn có xu hướng “đi cùng nhau”
- Hiểu cấu trúc kỹ năng học tập (tự nhiên – xã hội – ngoại ngữ)
- Hỗ trợ phân tích chiến lược học tập liên môn

### How (Trực quan hóa)
- Heatmap ma trận tương quan (Correlation Matrix)
- Màu sắc thể hiện mức độ liên hệ từ âm → dương

---

## 2. Sự khác biệt giữa Hà Nội và TP.HCM theo từng môn như thế nào?

### What (Dữ liệu)
- Điểm trung bình của từng môn học (Toán, Ngữ Văn, Ngoại Ngữ)
- Dữ liệu thí sinh thuộc hai thành phố lớn: Hà Nội và TP.HCM
- Giá trị được tổng hợp theo từng môn và từng thành phố

### Why (Mục tiêu)
- So sánh trực tiếp chất lượng học tập giữa hai trung tâm giáo dục lớn nhất cả nước
- Xác định môn học nào thành phố nào đang có lợi thế hơn
- Đánh giá mức độ chênh lệch năng lực học tập theo từng môn
- Quan sát sự cạnh tranh giáo dục giữa hai khu vực đô thị lớn

### How (Trực quan hóa)
- Biểu đồ **Dumbbell (biểu đồ quả tạ)** để so sánh cặp giá trị
- Mỗi môn học được biểu diễn bằng hai điểm:
  - Hà Nội
  - TP.HCM
- Đường nối giữa hai điểm thể hiện **khoảng cách chênh lệch điểm trung bình**

--- 

## 3. Đề thi có phân hóa học sinh tốt hay không?

### What (Dữ liệu)
- Điểm trung bình từng môn
- Độ lệch chuẩn của điểm số theo môn
- Số lượng thí sinh theo từng môn

### Why (Mục tiêu)
- Đánh giá chất lượng đề thi theo 2 tiêu chí:
  - Độ khó (difficulty)
  - Khả năng phân loại học sinh (discrimination)
- Xác định môn nào dễ, môn nào khó, môn nào phân hóa tốt
- Hỗ trợ cải thiện thiết kế đề thi

### How (Trực quan hóa)
- Biểu đồ Quadrant (Điểm trung bình × Độ lệch chuẩn)
- Chia 4 vùng phân tích:
  - Dễ & phân hóa tốt
  - Khó & phân hóa tốt
  - Dễ & phân hóa kém
  - Khó & phân hóa kém
- Bubble size thể hiện số lượng thí sinh

---

# Tổng kết TAB 5

Tab 5 cung cấp góc nhìn **thống kê & cấu trúc dữ liệu giáo dục**, giúp:
- Hiểu mối quan hệ giữa các môn học
- So sánh chất lượng giữa các trung tâm lớn
- Đánh giá độ khó và khả năng phân hóa của đề thi