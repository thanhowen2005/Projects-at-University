let orders = [];

document.addEventListener('DOMContentLoaded', async () => {
  await fetchData(); // Gọi API và render lần đầu
  updateBodyHeightAndLine();
});

// Gọi API lấy danh sách đơn hàng
async function fetchData() {
  const orderRes = await fetch('/api/orders');
  orders = await orderRes.json();
  orders = sortOrdersByDateDesc(orders);
  renderOrders(orders);
}


function parseDateString(dateStr) {
  const [day, month, year] = dateStr.split('/').map(Number);
  return new Date(year, month - 1, day);
}

function sortOrdersByDateDesc(orders) {
  return orders.sort((a, b) => {
    const dateA = parseDateString(a.date);
    const dateB = parseDateString(b.date);
    return dateB - dateA;
  });
}


// Định dạng tiền
function formatCurrency(num) {
  return num.toLocaleString("vi-VN") + "đ";
}

// Render danh sách đơn hàng
function renderOrders(data) {
  const tbody = document.querySelector(".user-table tbody");
  tbody.innerHTML = "";

  data.forEach((order) => {
    const shipping = order.shipping || {};
    const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    const row = `
      <tr>
        <td>${order._id}</td>
        <td>${order.date}</td>
        <td>${shipping.name || "Không rõ"}</td>
        <td>${shipping.phone || "-"}</td>
        <td>${formatCurrency(total)}</td>
        <td>
          <a href="OrdManagDt.html?id=${order._id}" class="details-link">Chi tiết</a>
          <i class='bx bx-trash action-icon delete-icon' data-id="${order._id}" style="cursor:pointer"></i>
          <a href="OrdManagEdit.html?id=${order._id}">
            <i class='bx bx-edit-alt action-icon'></i>
          </a>
        </td>
      </tr>
    `;
    tbody.insertAdjacentHTML("beforeend", row);
  });

  setupDeleteHandlers();
}

// Gắn sự kiện xoá đơn hàng
function setupDeleteHandlers() {
  const deleteIcons = document.querySelectorAll(".delete-icon");
  deleteIcons.forEach(icon => {
    icon.addEventListener("click", async () => {
      const orderId = icon.dataset.id;
      const confirmed = confirm("Bạn có chắc chắn muốn xóa đơn hàng này?");
      if (!confirmed) return;

      await fetch(`/api/orders/${orderId}`, { method: "DELETE" });

      alert("✅ Đã xóa đơn hàng thành công!");
      await fetchData(); // Cập nhật lại dữ liệu từ server
    });
  });
}

// Lọc đơn hàng theo trạng thái
const select = document.querySelector(".order-filter-dropdown");
select.addEventListener("change", () => {
  const status = select.value;
  const filtered = status ? orders.filter(o => o.status === status) : orders;
  renderOrders(filtered);
});

// Tìm kiếm theo nhiều trường (mã đơn, tên KH, sđt, tổng tiền, ngày)
const searchInput = document.querySelector(".search_input-in-content");
searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.trim().toLowerCase();

  const filtered = orders.filter(order => {
    const shipping = order.shipping || {};
    const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    return (
      order._id?.toLowerCase().includes(keyword) ||
      order.date?.toLowerCase().includes(keyword) ||
      shipping.name?.toLowerCase().includes(keyword) ||
      shipping.phone?.toLowerCase().includes(keyword) ||
      total.toString().includes(keyword)
    );
  });

  renderOrders(filtered);
});

// Cập nhật chiều cao container
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

  container.style.height = maxHeight + 'px';
  line.style.width = (maxHeight - 55) + 'px';
}
