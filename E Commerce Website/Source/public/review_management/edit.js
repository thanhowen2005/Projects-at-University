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

// Chuyển ngày về định dạng HTML: yyyy-MM-dd
function formatDateForInput(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  if (isNaN(date)) return '';
  return date.toISOString().split('T')[0];
}

// Hàm điền dữ liệu review vào form
function fillFormInputs(review) {
  const productInput = document.getElementById('input-productid');
  const userInput = document.getElementById('input-userid');
  const ratingInput = document.getElementById('input-rating');
  const cmtInput = document.getElementById('input-cmt');
  const dateInput = document.getElementById('input-date');
  const statusInput = document.getElementById('input-status');

  if (productInput) productInput.value = review.productid || '';
  if (userInput) userInput.value = review.userid || '';
  if (ratingInput) ratingInput.value = review.rating || '';
  if (cmtInput) cmtInput.value = review.cmt || '';
  if (dateInput) dateInput.value = formatDateForInput(review.date);
  if (statusInput) {
  // Nếu review.status = 0 hoặc 1 thì set value, nếu không thì để rỗng
  if (review.status === 0 || review.status === 1) {
    statusInput.value = String(review.status);
  } else {
    statusInput.value = '';
  }
}
}

// Hàm gọi API cập nhật
async function updateReview(reviewId) {
  const productid = document.getElementById('input-productid')?.value.trim();
  const userid = document.getElementById('input-userid')?.value.trim();
  const rating = parseInt(document.getElementById('input-rating')?.value.trim());
  const cmt = document.getElementById('input-cmt')?.value.trim();
  const date = document.getElementById('input-date')?.value.trim();
  const status = parseInt(document.getElementById('input-status')?.value);
  if (!productid || !userid || !rating) {
    alert("Vui lòng điền đầy đủ thông tin bắt buộc.");
    return;
  }

  const confirmUpdate = confirm("Bạn có chắc muốn cập nhật review này?");
  if (!confirmUpdate) return;

  const updatedReview = { productid, userid, rating, cmt, date, status };
  try {
    const res = await fetch(`/api/reviews/${reviewId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      
      body: JSON.stringify(updatedReview)
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.message || 'Cập nhật thất bại');
    }

    alert('Cập nhật review thành công!');
    window.location.href = '/review_management/index.html';

  } catch (error) {
    console.error('Lỗi khi cập nhật review:', error);
    alert('Đã xảy ra lỗi khi cập nhật review.');
  }
}

// Hàm khởi tạo khi trang load
async function initEditPage() {
  const urlParams = new URLSearchParams(window.location.search);
  const reviewId = urlParams.get('reviewId');

  if (!reviewId) {
    alert("Không tìm thấy reviewId trong URL");
    return;
  }

  try {
    const res = await fetch(`/api/reviews/${reviewId}`);
    if (!res.ok) throw new Error("Không thể lấy dữ liệu review");

    const review = await res.json();
    fillFormInputs(review);

    const submitBtn = document.getElementById('submitReview');
    if (submitBtn) {
      submitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        updateReview(reviewId);
      });
    }

  } catch (error) {
    console.error("Lỗi khi lấy dữ liệu review:", error);
    alert("Không thể tải dữ liệu đánh giá.");
  }
}

// Gọi khi tài liệu đã sẵn sàng
window.addEventListener('load', updateBodyHeightAndLine);
document.addEventListener('DOMContentLoaded', initEditPage);
