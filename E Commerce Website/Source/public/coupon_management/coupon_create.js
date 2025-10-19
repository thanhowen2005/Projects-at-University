//// CẬP NHẬT KÍCH THƯỚC TRANG
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
  
  
  //// GỬI THÔNG TIN COUPON
  function getCouponFromForm() {

    const code = document.getElementById("coupon-code-input").value.trim();
    const percent = Number(document.getElementById("coupon-percent-input").value);
 
    if (!code || !percent) {
      alert("Vui lòng điền đầy đủ thông tin mã giảm giá.");
      return null;
    }
  
    const coupon = {
      code,
      percent,
    };
    return coupon;
  }
  
  async function addCoupon() {
    const confirmAdd = confirm("Bạn có chắc chắn muốn tạo mã giảm giá này?");
    if (!confirmAdd) return;
  
    const coupon = getCouponFromForm();
    if (!coupon) return;
  
    try {
      const response = await fetch('/api/coupons', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(coupon)
      });
  
      if (!response.ok) {
        alert("Tạo mã giảm giá thất bại!");
        return;
      }
  
      window.location.href = 'index.html';
    } catch (error) {
      console.error("Lỗi khi tạo mã giảm giá:", error);
      alert("Có lỗi xảy ra khi gửi dữ liệu.");
    }
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("submit-btn").addEventListener("click", addCoupon);
  });  