document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const reviewId = urlParams.get('id');

  if (!reviewId) return;

  try {
    const res = await fetch(`/api/reviews/${reviewId}`);
    if (!res.ok) throw new Error("Không thể lấy dữ liệu review");

    const review = await res.json();

    const values = document.querySelectorAll(".review-page .review-field .value");

    // Điền theo thứ tự:
    values[0].textContent = review._id || '';
    values[1].textContent = review.productid || '';
    values[2].textContent = review.userid || '';
    values[3].textContent = review.rating || '';
    values[4].textContent = review.cmt || '';
    values[5].textContent = review.date || '';
    if (review.status === 0) {
        values[6].textContent = 'Chờ xác nhận';
    } else if (review.status === 1) {
        values[6].textContent = 'Đã xác nhận';
    } else {
        values[6].textContent = '';
    }

  } catch (error) {
    console.error("Lỗi khi lấy review:", error);
    alert("Không thể tải dữ liệu đánh giá.");
  }
});



//Cập nhật chiều dài của trang
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

  // Cập nhật chiều cao cho container
  container.style.height = maxHeight + 'px';

  // Cập nhật chiều dài cho .line-4 dựa trên chiều cao container
  line.style.width = (maxHeight - 55) + 'px';
}
window.addEventListener('load', () => {
  updateBodyHeightAndLine();
});