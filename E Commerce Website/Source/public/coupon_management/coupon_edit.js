function getCouponIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id'); // từ ?id=abc123
}

function populateCoupon(coupon) {
  document.getElementById('coupon-code-input').value = coupon.code || '';
  document.getElementById('coupon-percent-input').value = coupon.percent || '';
}

// Cập nhật thông tin coupon
async function saveUpdatedCoupon() {
  const id = getCouponIdFromURL();
  const code = document.getElementById('coupon-code-input').value.trim();
  const percent = Number(document.getElementById('coupon-percent-input').value);
  if (!code || isNaN(percent)) {
    alert("Vui lòng nhập đầy đủ thông tin!");
    return;
  }

  const confirmUpdate = confirm("Bạn có chắc chắn muốn cập nhật coupon này?");
  if (!confirmUpdate) return;

  try {
    const response = await fetch(`/api/coupons/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code, percent})
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Cập nhật thất bại");
    }

    alert("Cập nhật thành công!");
  window.location.href = `coupon_edit.html?id=${id}`;
  } catch (err) {
    console.error("Lỗi cập nhật coupon:", err);
    alert("Lỗi khi cập nhật coupon: " + err.message);
  }
}

// Gọi API để lấy dữ liệu ban đầu
async function fetchCouponDetail(id) {
  try {
    const response = await fetch(`/api/coupons/${id}`);
    if (!response.ok) throw new Error("Không tìm thấy coupon");
    const coupon = await response.json();
    populateCoupon(coupon);
  } catch (err) {
    alert("Lỗi khi tải thông tin coupon: " + err.message);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const couponId = getCouponIdFromURL();
  if (!couponId) return alert("Thiếu ID coupon!");

  fetchCouponDetail(couponId);
  document.getElementById("submit-btn").addEventListener("click", saveUpdatedCoupon);
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