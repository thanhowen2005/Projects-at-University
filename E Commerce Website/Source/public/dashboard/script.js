const filterType = document.getElementById("filter-type");
const dayInput = document.getElementById("filter-day");
const monthInput = document.getElementById("filter-month");
const yearInput = document.getElementById("filter-year");

// Cập nhật hiển thị ô chọn ngày / tháng / năm
filterType.addEventListener("change", () => {
  const type = filterType.value;
  dayInput.style.display = type === "day" ? "inline-block" : "none";
  monthInput.style.display = type === "month" ? "inline-block" : "none";
  yearInput.style.display = type !== "day" && type !== "all" ? "inline-block" : "none";
  updateStats();
});

dayInput.addEventListener("change", updateStats);
monthInput.addEventListener("change", updateStats);
yearInput.addEventListener("input", updateStats);

// Hàm lấy ngày theo định dạng dd/mm/yyyy hoặc mm/yyyy hoặc yyyy
function getFilterDate(type) {
  if (type === "day") {
    return dayInput.value.split("-").reverse().join("/");
  } else if (type === "month") {
    return `${String(monthInput.value).padStart(2, "0")}/${yearInput.value}`;
  } else if (type === "year") {
    return `${yearInput.value}`;
  } else {
    return null; // "all"
  }
}

// Hàm tính toán doanh thu, số lượng sản phẩm, số đơn hàng
async function updateStats() {
  const type = filterType.value;
  const filterDate = getFilterDate(type);

  try {
    const res = await fetch('/api/orders');
    const orders = await res.json();

    let totalRevenue = 0;
    let totalSold = 0;
    let totalOrders = 0;

    orders.forEach(order => {
      // Chỉ tính đơn đã xác nhận hoặc hoàn thành
      if (order.status !== "2" && order.status !== "3" && order.status !== "4") return;

      // Kiểm tra ngày phù hợp theo bộ lọc
      let match = false;
      if (type === "day" && order.date === filterDate) match = true;
      if (type === "month" && order.date.endsWith(filterDate)) match = true;
      if (type === "year" && order.date.endsWith("/" + filterDate)) match = true;
      if (type === "all") match = true;

      if (match) {
        totalOrders++;
        order.items.forEach(item => {
          totalSold += item.quantity;
          totalRevenue += item.price * item.quantity;
        });
      }
    });

    // Cập nhật kết quả ra giao diện
    document.getElementById("total-revenue").textContent = totalRevenue.toLocaleString("vi-VN") + " VND";
    document.getElementById("products-sold").textContent = totalSold;
    document.getElementById("total-orders").textContent = totalOrders;

  } catch (err) {
    console.error("Lỗi khi tải đơn hàng:", err);
  }
}

// Gọi hàm khi trang vừa tải xong
document.addEventListener("DOMContentLoaded", updateStats);
