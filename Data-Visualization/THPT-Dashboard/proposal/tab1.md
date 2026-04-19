# Tab 1: Tổng quan dữ liệu kỳ thi THPT qua các năm


## 1. Quy mô thí sinh thay đổi như thế nào qua các năm?

### What (Data)
- SBD (mã thí sinh – Unique Identifier)
- Năm (Ordered / Time dimension)

### Why (Task)
- **Summarize**: Tổng hợp số lượng thí sinh theo từng năm  
- **Identify Trend**: Nhận diện xu hướng tăng/giảm quy mô giáo dục qua thời gian  

Mục tiêu là giúp người dùng hiểu được bức tranh phát triển hoặc thu hẹp của hệ thống giáo dục qua các kỳ thi.

### How (Visual)
- **Area Chart (Biểu đồ miền)**

### Biện luận
Biểu đồ miền giúp nhấn mạnh yếu tố “khối lượng”, từ đó thể hiện trực quan quy mô thí sinh theo thời gian. Mắt người dễ dàng nhận ra sự mở rộng hoặc thu hẹp thông qua diện tích thay đổi qua từng năm, thay vì chỉ nhìn vào các con số rời rạc.

## 2. Môn học nào có kết quả cao nhất và thấp nhất trong năm được chọn?

### What (Data)
- Tên môn học (Categorical)
- Điểm trung bình môn (Quantitative)

### Why (Task)
- **Rank**: Xếp hạng các môn theo điểm trung bình  
- **Compare**: So sánh hiệu suất giữa các môn học  

Mục tiêu là xác định môn học nào có kết quả tốt nhất và môn nào đang là “vùng trũng” trong năm được chọn.

### How (Visual)
- **Clustered Bar Chart (Biểu đồ cột ngang)**

### Biện luận
Biểu đồ cột ngang giúp hiển thị đầy đủ tên môn học mà không bị cắt chữ, đặc biệt với các môn dài như “Ngoại ngữ” hay “Ngữ văn”. Việc sắp xếp giảm dần theo điểm trung bình giúp người dùng nhanh chóng nhận diện các giá trị cực trị mà không cần đọc từng số liệu chi tiết.

## 3. Thí sinh đang ưu tiên lựa chọn tổ hợp KHTN hay KHXH?

### What (Data)
- Tổ hợp môn (Categorical)
  - Được suy ra từ các cột điểm theo nhóm môn

### Why (Task)
- **Analyze Composition**: Phân tích cơ cấu lựa chọn tổ hợp thi của thí sinh  

Mục tiêu là nhận diện xu hướng chọn khối thi (Khoa học Tự nhiên vs Khoa học Xã hội), phục vụ phân tích định hướng tuyển sinh và giáo dục đại học.

### How (Visual)
- **Donut Chart (Biểu đồ vòng cung)**

### Biện luận
Biểu đồ donut phù hợp để thể hiện tỷ lệ thành phần trong một tổng thể. Khi kết hợp với bộ lọc theo năm, biểu đồ cho phép quan sát sự thay đổi trong hành vi lựa chọn tổ hợp qua thời gian. Đặt cạnh biểu đồ hiệu suất môn học giúp tạo ra góc nhìn đối chiếu:
- Học sinh chọn khối nào nhiều nhất?
- Và họ đang học tốt ở những môn nào?

---

# Tổng kết Tab 1

Tab 1 đóng vai trò là lớp “overview layer” của toàn bộ dashboard, giúp người dùng:
- Hiểu quy mô thí sinh theo thời gian
- Nắm bắt hiệu suất học tập theo môn
- Nhận diện xu hướng chọn tổ hợp thi

Đây là nền tảng để dẫn dắt sang các tab phân tích sâu hơn trong dashboard.