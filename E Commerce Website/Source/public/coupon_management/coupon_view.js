// Lấy thông tin coupon cần xem
function getCouponIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id'); // Lấy id từ ?id=...
}

function getCouponIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

async function getCouponFromURL() {
  const id = getCouponIdFromURL();
  if (!id) throw new Error('No coupon ID in URL');

  const res = await fetch(`/api/coupons/${id}`);
  if (!res.ok) throw new Error('Coupon not found');

  return await res.json();
}

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

function fillCouponInfo(coupon) {
  const percentEl = document.getElementById("coupon-percent");
  if (percentEl) percentEl.textContent = coupon.percent ? coupon.percent + "%" : "0%";

  const codeEl = document.getElementById("coupon-code");
  if (codeEl) codeEl.textContent = coupon.code || "";
}

document.addEventListener('DOMContentLoaded', async () => {
  try {
    updateBodyHeightAndLine();
    const coupon = await getCouponFromURL();
    fillCouponInfo(coupon);
  } catch (error) {
    console.error(error);
  }
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