// Lấy ID đơn hàng từ URL
function getOrderIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

// Định dạng tiền tệ
function formatCurrency(num) {
  return num.toLocaleString("vi-VN") + " đ";
}

// Cập nhật chiều cao trang
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

// Khi trang sẵn sàng
document.addEventListener("DOMContentLoaded", async () => {
  const orderId = getOrderIdFromURL();
  if (!orderId) return;

  const resOrder = await fetch(`/api/orders/${orderId}`);
  if (!resOrder.ok) {
    alert("Không tìm thấy đơn hàng");
    return;
  }
  const order = await resOrder.json();

  // Lấy thông tin giao hàng từ order.shipping
  const shipping = order.shipping || {};

  // Hiển thị thông tin người nhận
  document.getElementById("name").value = shipping.name || "";
  document.getElementById("email").value = shipping.email || "";
  document.getElementById("phone").value = shipping.phone || "";
  document.getElementById("address").value = shipping.address || "";

  // Hiển thị danh sách sản phẩm
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
    <div class="order-date">Ngày mua hàng: <span class="date-text">${order.date}</span></div>
  `;

  // Hiển thị trạng thái hiện tại
  document.getElementById("statusSelect").value = order.status.toString();

  updateBodyHeightAndLine();

  // Lưu trạng thái mới
  document.getElementById("saveBtn").addEventListener("click", async () => {
    const newStatus = document.getElementById("statusSelect").value;

    const confirmed = confirm("Bạn có chắc chắn muốn cập nhật trạng thái đơn hàng?");
    if (!confirmed) return;

    await fetch(`/api/orders/${orderId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ status: newStatus })
    });

    alert("✅ Trạng thái đơn hàng đã được cập nhật!");
  });
});
