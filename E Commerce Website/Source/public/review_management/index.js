let reviews = [];
let users = [];
let products = [];

document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Fetch đồng thời reviews, users, products
    const [resReviews, resUsers, resProducts] = await Promise.all([
      fetch('/api/reviews'),
      fetch('/users'),
      fetch('/api/products')
    ]);
    reviews = await resReviews.json();
    users = await resUsers.json();
    products = await resProducts.json();

    reviews.sort((a, b) => parseDate(b.date) - parseDate(a.date));

    renderReviews(reviews);
    updateBodyHeightAndLine();
  } catch (error) {
    console.error('Lỗi khi tải dữ liệu:', error);
    alert('Lỗi khi tải dữ liệu. Vui lòng thử lại.');
  }
});


function parseDate(str) {
  if (!str) return new Date(0);

  if (str.includes('/')) {
    // định dạng dd/mm/yyyy
    const parts = str.trim().split('/');
    if (parts.length !== 3) return new Date(0);
    const [d, m, y] = parts.map(Number);X``
    return new Date(y, m - 1, d);
  } else if (str.includes('-')) {
    // định dạng yyyy-mm-dd
    return new Date(str);
  }

  return new Date(0);
}



// Hàm lấy tên người dùng theo userId
function getUserNameById(userId) {
  const user = users.find(u => u._id === userId);
  return user ? user.name : '(Không rõ người dùng)';
}

// Hàm lấy tên sản phẩm theo productId
function getProductNameById(productId) {
  const product = products.find(p => p._id === productId);
  return product ? product.name : '(Không rõ sản phẩm)';
}

// Cập nhật chiều cao trang và line
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

function renderReviews(reviews) {
  const productList = document.querySelector('.list-product');
  productList.innerHTML = ''; // Xóa nội dung cũ

  reviews.forEach(review => {
    const userName = getUserNameById(review.userid);
    const productName = getProductNameById(review.productid);

    const productElement = document.createElement('div');
    productElement.className = 'frame-940';

    productElement.innerHTML = `
      <a class="edit" href="edit.html?reviewId=${review._id}">
        <img src="images/edit.svg" alt="Edit" />
      </a>
      <button class="btn delete">
        <img src="images/delete.svg" alt="Delete" />
      </button>

      <a class="details" href="/review_management/view.html?id=${review._id}">Chi tiết</a>

      <div class="product-date"> ${review.date}</div>
      <div class="product-rating">${review.rating}</div>
      <div class="product-id">${review._id}</div>
      <div class="product-userid">${userName}</div>
      <div class="product-productid">${productName}</div>
    `;

    const deleteBtn = productElement.querySelector('.btn.delete');
    deleteBtn.addEventListener('click', async () => {
      if (confirm(`Bạn có chắc muốn xóa đánh giá "${review._id}" không?`)) {
        await deleteReview(review._id);
      }
    });

    productList.appendChild(productElement);
  });
}

// Hàm xóa review
async function deleteReview(reviewId) {
  try {
    const response = await fetch(`/api/reviews/${reviewId}`, { method: 'DELETE' });

    if (!response.ok) {
      alert('Xóa đánh giá thất bại!');
      return;
    }

    // Load lại danh sách đánh giá mới
    const refreshedResponse = await fetch('/api/reviews');
    reviews = await refreshedResponse.json();

    renderReviews(reviews);
    updateBodyHeightAndLine();

  } catch (error) {
    alert('Lỗi khi xóa đánh giá');
    console.error(error);
  }
}

const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearSearch');

searchInput.addEventListener('input', () => {
  const keyword = searchInput.value.toLowerCase().trim();

  const filtered = reviews.filter(review => {
    const userName = getUserNameById(review.userid).toLowerCase();
    const productName = getProductNameById(review.productid).toLowerCase();

    return review._id.toLowerCase().includes(keyword) ||
           userName.includes(keyword) ||
           productName.includes(keyword) ||
           review.date.toLowerCase().includes(keyword);
  });

  renderReviews(filtered);
  updateBodyHeightAndLine();
});

clearBtn.addEventListener('click', () => {
  searchInput.value = '';
  renderReviews(reviews);
  updateBodyHeightAndLine();
});

const statusFilter = document.getElementById('status-filter');

statusFilter.addEventListener('change', () => {
  const selectedStatus = statusFilter.value; // "all", "0", "1"

  let filteredReviews;

  if (selectedStatus === 'all') {
    filteredReviews = reviews;
  } else {
    filteredReviews = reviews.filter(review => String(review.status) === selectedStatus);
  }

  renderReviews(filteredReviews);
  updateBodyHeightAndLine();
});
