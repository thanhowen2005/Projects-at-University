document.addEventListener("DOMContentLoaded", async () => {
  document.getElementById('orderLink').style.color = '#db4444';

  const user = getUserFromLocalStorage();
  if (!user || !user.email) {
    alert("Vui lòng đăng nhập để xem đơn hàng.");
    return;
  }

  try {
    const [orders, coupons] = await Promise.all([fetchOrders(), fetchCoupons()]);
    const enrichedOrders = enrichOrdersWithCoupon(orders, coupons);
    const userOrders = filterOrdersByEmail(enrichedOrders, user.email); 
    renderOrders(userOrders);
  } catch (error) {
    console.error("Lỗi khi tải đơn hàng hoặc mã giảm giá:", error);
  }

  updateBodyHeight();
});


function getUserFromLocalStorage() {
  return JSON.parse(localStorage.getItem("user"));
}

async function fetchOrders() {
  const res = await fetch("http://localhost:3000/api/orders");
  if (!res.ok) throw new Error("Không lấy được danh sách đơn hàng.");
  return await res.json();
}


async function fetchCoupons() {
  const res = await fetch("http://localhost:3000/api/coupons");
  if (!res.ok) throw new Error("Không lấy được danh sách coupon.");
  return await res.json();
}


function enrichOrdersWithCoupon(orders, coupons) {
  return orders.map(order => {
    const coupon = coupons.find(c => c._id === order.couponId);
    return {
      ...order,
      coupon: coupon || null
    };
  });
}



// Dùng email trong shipping để lọc
function filterOrdersByEmail(orders, email) {
  return orders.filter(order => order.shipping?.email === email);
}

function parseDateString(dateStr) {
  const [day, month, year] = dateStr.split('/').map(Number);
  return new Date(year, month - 1, day);
}

function sortOrdersByDateDesc(orders) {
  return orders.sort((a, b) => parseDateString(b.date) - parseDateString(a.date));
}

function renderOrders(orders) {
  const sortedOrders = sortOrdersByDateDesc(orders);
  const container = document.querySelector(".product-list");
  container.innerHTML = "";

  sortedOrders.forEach((order, index) => {
    const total = calculateOrderTotal(order.items, order.coupon);
    const couponHTML = order.coupon
      ? `<div class="order-coupon">Mã giảm giá: <span class="coupon-text">${order.coupon.code} (-${order.coupon.percent}%)</span></div><br>`
      : "";

    const itemsHTML = renderOrderItems(order.items);
    
    const bgColor = index % 2 === 0 ? "#f9f9f9" : "#ffffff";

    const orderHTML = `
      <div class="order" style="background-color: ${bgColor}; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: box-shadow 0.3s ease;">
        <h3>Đơn hàng #${order._id}</h3>
        <div class="product-list">${itemsHTML}</div>
        ${couponHTML}
        <div class="order-total">Tổng cộng: <span class="total-text">${total.toLocaleString()} đ</span></div><br>
        <div class="order-date">Ngày mua hàng: <span class="date-text">${order.date}</span></div><br>
        <div class="order-status">Trạng thái: <span class="status-text">${getOrderStatus(order.status)}</span></div>
      </div>
    `;

    container.innerHTML += orderHTML;
  });

  const orderElements = container.querySelectorAll('.order');
  orderElements.forEach(orderEl => {
    orderEl.addEventListener('mouseenter', () => {
      orderEl.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";
    });
    orderEl.addEventListener('mouseleave', () => {
      orderEl.style.boxShadow = "0 2px 5px rgba(0,0,0,0.1)";
    });
  });
}

function renderOrderItems(items) {
  return items.map(item => `
    <div class="cart-item">
      <img src="${item.image}" alt="${item.name}" class="product-image">
      <span class="product-name">${item.name}</span>
      <span class="product-qty">x${item.quantity}</span>
      <span class="product-price">${item.price.toLocaleString()} đ</span>
    </div>
  `).join("");
}

function calculateOrderTotal(items, coupon) {
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  if (coupon?.percent) {
    return total - (coupon.percent / 100) * total;
  }
  return total;
}

function getOrderStatus(statusCode) {
  switch (statusCode) {
    case "1": return "Chờ xác nhận";
    case "2": return "Đã xác nhận";
    case "3": return "Đang giao";
    case "4": return "Đã giao";
    default: return "Không rõ";
  }
}

function updateBodyHeight() {
  const container = document.querySelector('.body');
  if (!container) return;

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

  const viewportHeight = window.innerHeight;
  const finalHeight = Math.max(maxHeight, viewportHeight);
  container.style.height = finalHeight + 100 + 'px';
}
