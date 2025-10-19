// Lấy productId từ URL (?id=...)
const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get("id");

// Biến để chứa danh sách sản phẩm liên quan (sẽ gán sau)
let relatedProducts = [];

Promise.all([
  fetch(`http://localhost:3000/api/products/${productId}`).then(res => res.json()),
  fetch("http://localhost:3000/api/reviews").then(res => res.json()),
  fetch("http://localhost:3000/users").then(res => res.json()),
  fetch("http://localhost:3000/api/products").then(res => res.json()) // fetch tất cả sản phẩm để lọc related
])
.then(([productData, reviewsData, usersData, allProducts]) => {
  window.main_product = productData;
  window.reviews = reviewsData.filter(r => r.status === 1);;
  window.users = usersData;

  //Thay đổi trang web khi đăng xuất
  const guestLink = document.getElementById('logout-link');
  guestLink.href = `../detailPage/index.html?id=${main_product._id}`;

  // Hàm tính giá sau giảm giá
  function getDiscountedPrice(product) {
    return product.discount
      ? product.price * (1 - product.discount / 100)
      : product.price;
  }

  const mainPrice = getDiscountedPrice(main_product);

  // Lọc sản phẩm liên quan theo giá ±5 triệu, cùng category, loại bỏ sản phẩm chính
  relatedProducts = allProducts.filter(p =>
    p._id !== main_product._id &&
    p.category === main_product.category &&
    Math.abs(getDiscountedPrice(p) - mainPrice) <= mainPrice * 0.3
  );

  if (relatedProducts.length < 4) {
    const existingIds = new Set(relatedProducts.map(p => p._id));

    const extraProducts = allProducts.filter(p =>
      p._id !== main_product._id &&
      p.specs[0] === main_product.specs[0]
    );

    relatedProducts = [...relatedProducts, ...extraProducts].slice(0, 8); 
  }

  // Gọi các hàm xử lý UI
  replaceProductInfo(main_product);
  updateProductInfo(main_product);
  renderReviewsForProduct(main_product._id);
  renderRelatedProducts(relatedProducts);
        updateBodyHeight()
})
.catch(err => console.error("Lỗi khi fetch dữ liệu:", err));




// Tính chiều dài của trang
function resize() {
  const p = document.querySelector('.product-details-page');
  let max = 0;
  p.querySelectorAll('*').forEach(el => {
    const b = el.getBoundingClientRect();
    const t = p.getBoundingClientRect().top;
    max = Math.max(max, b.bottom - t);
  });
  p.style.minHeight = max + 20 + 'px';
}
window.onload = resize;
window.onresize = resize;



// Hàm thay thông tin sản phẩm trên HTML hiện tại
function replaceProductInfo(product) {
  // Thay hình ảnh chính
  const mainImg = document.getElementById('main-image');
  mainImg.src = product.images[0];

  // Thay các ảnh phụ (4 ảnh đầu)
  const thumbnails = document.querySelectorAll(".frame-895 img, .frame-896 img, .frame-897 img, .frame-919 img");
  thumbnails.forEach((thumb, index) => {
    if (product.images[index]) {
      const fixedImagePath = product.images[index].replace(/\\/g, "/");
      const fullPath = fixedImagePath.startsWith("/") ? fixedImagePath : "/" + fixedImagePath;
 
      thumb.src = fullPath
      thumb.parentElement.setAttribute("onclick", `changeImage('${fullPath}')`);
    }
  });

  // Thay tên sản phẩm
  document.querySelector(".macbookair").textContent = product.name;

  // Thay giá sản phẩm
  document.querySelector(".product-price").textContent = (product.price - product.discount/100*product.price).toLocaleString("vi-VN") + "đ";

  // Thay mô tả sản phẩm
  document.querySelector(".macbook").textContent = product.description;

  // Thêm số lượng sản phẩm còn lại

  if (main_product.stock === 0) {
      document.querySelector(".stock").textContent = "Sản phẩm hiện không có sẵn"

    // Ẩn div có class "frame-906"
    const frameDiv = document.querySelector(".frame-926");
    if (frameDiv) frameDiv.style.display = "none";

    // Ẩn div có class "button"
    const buttonDiv = document.querySelector(".button");
    if (buttonDiv) buttonDiv.style.display = "none";
  }
  else
    document.querySelector(".stock").textContent = "Số lượng có sẵn: " + main_product.stock;

}

// Thay đổi ảnh chính
function changeImage(imageSrc) {
  document.getElementById('main-image').src = imageSrc;
}


// Tăng/giảm số lượng sản phẩm
const btnMinus = document.getElementById('btn-minus');
const btnPlus = document.getElementById('btn-plus');
const quantity = document.getElementById('quantity');

btnMinus.addEventListener('click', () => {
  let current = parseInt(quantity.textContent);
  if (current > 1) {
    quantity.textContent = current - 1;
  }
});

btnPlus.addEventListener('click', () => {
  let current = parseInt(quantity.textContent);
  const stock = window.main_product?.stock || 1;

  if (current < stock) {
    quantity.textContent = current + 1;
  }
});

// Thêm vào giỏ hàng
function showNotification() {
  const notification = document.getElementById("notification");
  notification.classList.add("show");

  setTimeout(() => {
    notification.classList.remove("show");
  }, 3000);
}


//Thông tin main-product
const specTitleMap = {
  Mouse: [
    "Thương hiệu", "Bảo hành", "Màu sắc", "Độ phân giải", "Pin",
    "Bộ nhớ", "Kích thước", "Trọng lượng"
  ],
  Keyboard: [
    "Thương hiệu", "Bảo hành", "Màu sắc", "Layout", "Pin",
    "Switch", "LED", "Kết nối", "Keycap", "Trọng lượng"
  ],
  Laptop: [
    "Thương hiệu", "Bảo hành", "Màu sắc", "CPU", "GPU", "Màn hình",
    "RAM", "SSD", "Camera", "Pin", "Trọng lượng"
  ],
  LaptopGaming: [
    "Thương hiệu", "Bảo hành", "Màu sắc", "CPU", "GPU", "Màn hình",
    "RAM", "SSD", "Camera", "Pin", "Trọng lượng"
  ]
};

function updateProductInfo(p) {
  const specTitles = specTitleMap[p.category] || [];

  const specsHTML = p.specs.map((v, i) => `
    <tr><th>${specTitles[i] || `Thuộc tính ${i+1}`}</th><td>${v}</td></tr>
  `).join('');
  const highlights = p.highlights.map(h => `<div class="highlight-item">${h}</div>`).join('');

  document.getElementById("product-detail").innerHTML = `
    <div class="frame-9252">
      <div class="frame-923">
        <div class="category-rectangle"><div class="rectangle-17"></div></div>
        <div class="product-information">Thông tin sản phẩm</div>
      </div>
    </div>
    <table class="specs-table"><tbody>${specsHTML}</tbody></table>
    <div class="frame-9252">
      <div class="frame-923">
        <div class="category-rectangle"><div class="rectangle-17"></div></div>
        <div class="product-information">Điểm nổi bật</div>
      </div>
      <div class="highlights-list">${highlights}</div>
    </div>
  `;
}


// Scroll trái/phải
function setupHorizontalScroll(containerId, btnLeftId, btnRightId, scrollAmount = 300) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const btnLeft = document.getElementById(btnLeftId);
  const btnRight = document.getElementById(btnRightId);

  if (btnLeft) {
    btnLeft.addEventListener("click", () => {
      container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    });
  }

  if (btnRight) {
    btnRight.addEventListener("click", () => {
      container.scrollBy({ left: scrollAmount, behavior: "smooth" });
    });
  }
}

// Gọi hàm khi DOM load xong
document.addEventListener("DOMContentLoaded", () => {
  setupHorizontalScroll("related-products", "btn-left", "btn-right", 300);
});



function getAverageRating(productId) {
  const filtered = reviews.filter(r => r.productid === productId);
  if (filtered.length === 0) return { avg: 0, count: 0 };
  const total = filtered.reduce((sum, r) => sum + r.rating, 0);
  const avg = total / filtered.length;
  return { avg, count: filtered.length };
}

function renderStars(rating) {
  let stars = '';
  const fullStars = Math.floor(rating);
  for (let i = 0; i < fullStars; i++) {
    stars += `<img class="five-star2" src="image/star.png" />`;
  }
  return stars;
}

function renderRelatedProducts(products) {
  const container = document.getElementById("related-products");
  if (!container) return;
  container.innerHTML = "";

  products.forEach(p => {
    newPrice = p.price - p.price*p.discount/100
    const { avg, count } = getAverageRating(p._id);

    container.innerHTML += `
      <div class="cart-with-flat-discount">
        <a href="../detailPage/index.html?id=${p._id}">
        <div class="frame-570">
          ${p.discount ? `<div class="discount-percent"><div class="percent-number">-${p.discount}%</div></div>` : ""}
          <div class="frame-613">
            <img class="image-product-related" src="${p.images?.[0] || 'image/default.png'}" alt="${p.name}" />
          </div>
        </div>
        <div class="frame-569">
          <div class="product-name">${p.name}</div>
          <div class="frame-567">
            <div class="new-price">${newPrice.toLocaleString("vi-VN")}₫</div>
            ${p.price ? `<div class="old-price">${p.price.toLocaleString("vi-VN")}₫</div>` : ""}
          </div>
          <div class="frame-566">
            ${renderStars(avg)}
            <div class="star">(${count})</div>
          </div>
        </div>
        </a>
      </div>
    `;
  });
}


// Số lượng đánh giá cho main-product ở phần review
function renderStarWithRating(rating) {
  let stars = "";
  for (let i = 0; i < rating; i++) {
    stars += `<img src="image/star.png" alt="star icon" class="star-icon" />`;
  }
  return `
    <div class="stars-wrapper">
      ${stars}
    </div>
  `;
}

function getUserNameById(userId) {
  const user = users.find(u => u._id === userId);
  return user ? user.name : "Người dùng ẩn danh";
}

// Thay đổi số lượng đánh giá và số sao trung bình trên phần title sản phẩm
function renderAverageStars(averageRating, totalReviews) {
  const starsContainer = document.querySelector(".dynamic-stars");
  const totalReviewsText = document.querySelector(".total-reviews-text");

  // Làm tròn xuống để lấy số sao nguyên
  const rounded = Math.round(averageRating);

  // Render đúng số lượng sao
  let starsHTML = "";
  for (let i = 0; i < rounded; i++) {
    starsHTML += `<img src="image/star.png" alt="star icon" class="star-icon" />`;
  }

  starsContainer.innerHTML = starsHTML;
  totalReviewsText.textContent = `(${totalReviews} Đánh giá)`;
}


function renderReviewsForProduct(productId) {
  const reviewsContainer = document.querySelector(".reviews-list");
  const ratingNumberEl = document.querySelector(".average-rating .rating-number");
  const totalReviewsEl = document.querySelector(".average-rating .total-reviews");

  const filteredReviews = reviews.filter(r => r.productid === productId);
  const totalReviews = filteredReviews.length;
  const totalRating = filteredReviews.reduce((sum, r) => sum + r.rating, 0);
  const averageRating = totalReviews > 0 ? (totalRating / totalReviews).toFixed(1) : "0.0";

  // Cập nhật thống kê
  ratingNumberEl.textContent = averageRating;
  totalReviewsEl.textContent = `(${totalReviews} đánh giá)`;

  // Xoá cũ
  reviewsContainer.innerHTML = "";

  
  // Cập nhật số reviews trên title
  renderAverageStars(averageRating, totalReviews);

  if (totalReviews === 0) {
    reviewsContainer.innerHTML = "<p>Chưa có đánh giá nào cho sản phẩm này.</p>";
    return;
  }


  filteredReviews.forEach(review => {
    const reviewerName = getUserNameById(review.userid);
    const reviewItem = document.createElement("article");
    reviewItem.className = "review-item";
    reviewItem.innerHTML = `
      <header class="review-header">
        <h3 class="review-user">${reviewerName}</h3>
        <div class="review-stars">
          ${renderStarWithRating(review.rating)}
        </div>
      </header>
      <p class="review-text">${review.cmt}</p>
    `;
    reviewsContainer.appendChild(reviewItem);
  });
}


// Đánh giá sản phẩm
document.addEventListener('DOMContentLoaded', () => {
  const submitBtn = document.getElementById('submit-comment');
  const ratingSelect = document.getElementById('rating-select');
  const commentText = document.getElementById('comment-text');


  submitBtn.addEventListener('click', async () => {
    const isConfirmed = confirm('Bạn có chắc muốn gửi đánh giá này không?');
    if (!isConfirmed) return;

    const user = window.currentUser || JSON.parse(localStorage.getItem("user"));
    if (!user) {
      alert('Bạn cần đăng nhập để gửi đánh giá.');
      return;
    }

    const rating = Number(ratingSelect.value);
    const cmt = commentText.value.trim();

    if (!rating) {
      alert('Vui lòng chọn số sao đánh giá.');
      return;
    }

    if (!window.main_product || !window.main_product._id) {
      alert('Không tìm thấy sản phẩm để đánh giá.');
      return;
    }

    const reviewData = {
      productid: window.main_product._id,
      userid: user._id || user.id || '',
      rating,
      cmt,
      date: new Date().toISOString().slice(0, 10),
      status: 0
    };

    try {
      const response = await fetch('http://localhost:3000/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reviewData)
      });

      if (!response.ok) throw new Error('Lỗi khi gửi đánh giá.');

      alert('Gửi đánh giá thành công! Đang chờ xác nhận.');
      ratingSelect.value = '';
      commentText.value = '';

      renderReviewsForProduct(window.main_product._id);
    } catch (error) {
      console.error(error);
      alert('Có lỗi xảy ra khi gửi đánh giá. Vui lòng thử lại sau.');
    }
  });
});


// Cập nhật chiều cao trang
function updateBodyHeight() {
  const container = document.querySelector('.body');
  if (!container) return;

  let maxHeight = 0;
  const containerRect = container.getBoundingClientRect();
  container.querySelectorAll('*').forEach(el => {
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
}


