// Hàm đọc orderId từ URL
function getOrderIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// Định dạng tiền
function formatCurrency(num) {
  return num.toLocaleString("vi-VN") + " đ";
}

// Trạng thái đơn hàng
function getOrderStatus(statusCode) {
  switch (statusCode) {
    case "1": return "Chờ xác nhận";
    case "2": return "Đã xác nhận";
    case "3": return "Đang giao";
    case "4": return "Đã giao";
    default: return "Không rõ";
  }
}

// Cập nhật chiều cao
function updateBodyHeightAndLine() {
  const container = document.querySelector('.body');
  const line = document.querySelector('.line-4');
  if (!container || !line) return;

  let maxHeight = 0;
  const allChildren = container.querySelectorAll('*');
  const containerRect = container.getBoundingClientRect();

  allChildren.forEach(el => {
    const style = window.getComputedStyle(el);
    let elBottom;
    if (style.position === 'absolute' || style.position === 'fixed') {
      elBottom = el.offsetTop + el.offsetHeight;
    } else {
      const rect = el.getBoundingClientRect();
      elBottom = rect.bottom - containerRect.top;
    }

    if (elBottom > maxHeight) maxHeight = elBottom;
  });

  container.style.height = maxHeight + 100 + 'px';
  line.style.width = (maxHeight - 55) + 100 + 'px';
}

// Main logic
document.addEventListener("DOMContentLoaded", async () => {
  const orderId = getOrderIdFromURL();
  if (!orderId) return;

  const resOrder = await fetch(`/api/orders/${orderId}`);
  if (!resOrder.ok) {
    alert("Không tìm thấy đơn hàng");
    return;
  }
  const order = await resOrder.json();

  // Lấy thông tin shipping từ order
  const shipping = order.shipping || {};

  // Gán thông tin giao hàng
  document.getElementById("name").value = shipping.name || "";
  document.getElementById("email").value = shipping.email || "";
  document.getElementById("phone").value = shipping.phone || "";
  document.getElementById("address").value = shipping.address || "";

  // Gán chi tiết đơn hàng
  const orderContainer = document.getElementById("orderDetails");
  let total = 0;

  const productListHTML = order.items.map(item => {
    const lineTotal = item.price * item.quantity;
    total += lineTotal;
    return `
      <div class="cart-item">
        <img src="${item.image}" alt="${item.name}" class="product-image">
        <span class="product-name">${item.name}</span>
        <span class="product-qty">x${item.quantity}</span>
        <span class="product-price">${formatCurrency(item.price)}</span>
      </div>
    `;
  }).join("");

  orderContainer.innerHTML = `
    <div class="product-list">${productListHTML}</div>
    <div class="order-total">Tổng cộng: <span class="total-text">${formatCurrency(total)}</span></div><br>
    <div class="order-date">Ngày mua hàng: <span class="date-text">${order.date}</span></div><br>
    <div class="order-status">Trạng thái: <span class="status-text">${getOrderStatus(order.status)}</span></div>
  `;

  updateBodyHeightAndLine();
});
