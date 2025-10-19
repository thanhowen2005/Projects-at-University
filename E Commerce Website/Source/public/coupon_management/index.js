let coupons = [];

// Khi DOM đã sẵn sàng
document.addEventListener('DOMContentLoaded', async () => {
  const response = await fetch('/api/coupons');
  coupons = await response.json();

  renderCoupons(coupons);
  updateBodyHeightAndLine();
});

// Cập nhật chiều dài container
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

window.addEventListener('load', () => {
  updateBodyHeightAndLine();
});

// Hiển thị danh sách coupon
function renderCoupons(coupons) {
  const couponList = document.querySelector('.list-coupon');
  couponList.innerHTML = '';

  coupons.forEach(coupon => {
    const couponEl = document.createElement('div');
    couponEl.className = 'frame-940';

    couponEl.innerHTML = `
      <a class="edit" href="coupon_edit.html?id=${coupon._id}">
        <img src="images/edit.svg" alt="Edit" />
      </a>
      <button class="btn delete">
        <img src="images/delete.svg" alt="Delete" />
      </button>
      <a class="details" href="coupon_view.html?id=${coupon._id}">Chi tiết</a>
      <div class="coupon-id">${coupon._id}</div>
      <div class="coupon-code">${coupon.code}</div>
      <div class="coupon-percent">${coupon.percent}%</div>
    `;

    const deleteBtn = couponEl.querySelector('.btn.delete');
    deleteBtn.addEventListener('click', async () => {
      if (confirm(`Bạn có chắc muốn xóa coupon mã "${coupon.code}" không?`)) {
        await deleteCoupon(coupon._id);
      }
    });

    couponList.appendChild(couponEl);
  });
}

// Xóa coupon
async function deleteCoupon(couponId) {
  try {
    const response = await fetch(`/api/coupons/${couponId}`, { method: 'DELETE' });

    if (!response.ok) {
      alert('Xóa coupon thất bại!');
      return;
    }

    const refreshed = await fetch('/api/coupons');
    const updated = await refreshed.json();

    renderCoupons(updated);
    updateBodyHeightAndLine();

  } catch (err) {
    alert('Lỗi khi xóa coupon');
    console.error(err);
  }
}

// TÌM KIẾM
const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearSearch');

searchInput.addEventListener('input', () => {
  const keyword = searchInput.value.toLowerCase().trim();

  const filtered = coupons.filter(coupon =>
    coupon.code.toLowerCase().includes(keyword) ||
    coupon._id.toLowerCase().includes(keyword) ||
    (coupon.description && coupon.description.toLowerCase().includes(keyword))
  );

  renderCoupons(filtered);
  updateBodyHeightAndLine();
});

clearBtn.addEventListener('click', () => {
  searchInput.value = '';
  renderCoupons(coupons);
  updateBodyHeightAndLine();
});
