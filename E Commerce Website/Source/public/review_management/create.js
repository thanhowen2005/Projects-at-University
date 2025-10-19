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



/// Hàm thêm tạo review mới
async function createReview() {
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

    const confirmAdd = confirm("Bạn có chắc chắn muốn thêm review này?");
    if (!confirmAdd) return


    const newReview = { productid, userid, rating, cmt, date, status };
console.log("Dữ liệu gửi lên:", newReview);
    try {
    const res = await fetch('/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newReview)
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Tạo review thất bại');
    }

    alert('Tạo review thành công!');
    window.location.href = '/review_management/index.html';

    } catch (error) {
    console.error('Lỗi khi tạo review:', error);
    alert('Đã xảy ra lỗi khi gửi dữ liệu.');
    }
}


// Gọi hàm khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitReview');
    if (submitBtn) {
    submitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        createReview();
    });
    }
});