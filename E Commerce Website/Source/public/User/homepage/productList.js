// ==== FETCH DỮ LIỆU ====
Promise.all([
  fetch('http://localhost:3000/api/products').then(res => res.json()),
  fetch('http://localhost:3000/api/reviews').then(res => res.json())
])
.then(([products, reviews]) => {
  const reviewsByProductId = groupReviewsByProductId(reviews);

  renderTopDiscount(products, reviewsByProductId);
  renderCategoriesUI(); 
  renderTopSellingByCategory(products, reviewsByProductId, "product-list2", "laptop");
  renderTopSellingByCategory(products, reviewsByProductId, "product-list3", "laptopgaming");
  renderTopSellingByCategory(products, reviewsByProductId, "product-list4", "mouse");
  renderTopSellingByCategory(products, reviewsByProductId, "product-list5", "keyboard");
  attachScroll("product-list", ".icons-arrow-left", ".icons-arrow-right");
  attachScroll("product-list2", ".icons-arrow-left2", ".icons-arrow-right2");
  attachScroll("product-list3", ".icons-arrow-left3", ".icons-arrow-right3");
  attachScroll("product-list4", ".icons-arrow-left4", ".icons-arrow-right4");
  attachScroll("product-list5", ".icons-arrow-left5", ".icons-arrow-right5");

})
.catch(err => console.error(err));



function groupReviewsByProductId(reviews) {
  return reviews.reduce((acc, review) => {
    const pid = String(review.productid);
    if (!acc[pid]) acc[pid] = [];
    acc[pid].push(review);
    return acc;
  }, {});
}


function renderTopDiscount(products, reviewsByProductId) {
  const topDiscountProducts = [...products]
    .sort((a, b) => b.discount - a.discount)
    .slice(0, 10);

  const productContainer = document.getElementById("product-list");
  productContainer.innerHTML = "";

  topDiscountProducts.forEach(product => {
    productContainer.innerHTML += createProductHTML(product, reviewsByProductId);
  });
}


function renderTopSellingByCategory(products, reviewsByProductId, containerId, categoryName, limit = 10) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = "";

  const filtered = products
    .filter(p => p.category?.toLowerCase() === categoryName.toLowerCase())
    .filter(p => typeof p.sold === 'number')
    .sort((a, b) => b.sold - a.sold)
    .slice(0, limit);

  filtered.forEach(product => {
    container.innerHTML += createProductHTML(product, reviewsByProductId);
  });
}


function createProductHTML(product, reviewsByProductId) {
  const productReviews = reviewsByProductId[product._id] || [];
  const avgRating = productReviews.length
    ? (productReviews.reduce((sum, r) => sum + r.rating, 0) / productReviews.length).toFixed(1)
    : "Chưa có";

  return `
    <div class="best-selling-cart">
      <a href="../detailPage/index.html?id=${product._id}">
        <div class="frame-570">
          <div class="discount-percent">
            <div class="discount">${product.discount}%</div>
          </div>
          <div class="frame-611">
            <img class="product-img" src="${product.images?.[0] || 'fallback.png'}" />
          </div>
        </div>
        <div class="frame-569">
          <div class="product-name">${product.name}</div>
          <div class="frame-567">
            <div class="new-price">${(product.price - product.price * product.discount / 100).toLocaleString('vi-VN')}đ</div>
            <div class="old-price">${product.price.toLocaleString('vi-VN')}đ</div>
          </div>
          <div class="frame-566">
            <div class="star">
              <img src="./images/star.png" alt="star" style="width:16px; height:16px; vertical-align:middle;" />
              ${avgRating} (${productReviews.length})
            </div>
          </div>
        </div>
      </a>
    </div>
  `;
}



function renderCategoriesUI() {
  const categories = [
    { name: "Laptop", icon: "bx bx-laptop", link:  `../view_all_products_page/all_products.html?category=${encodeURIComponent('Laptop')}` },
    { name: "Laptop Gaming", icon: "bxr  bx-gaming", link: `../view_all_products_page/all_products.html?category=${encodeURIComponent('LaptopGaming')}` },
    { name: "Chuột", icon: "bxr  bx-mouse-alt", link: `../view_all_products_page/all_products.html?category=${encodeURIComponent('Mouse')}` },
    { name: "Bàn phím", icon: "bxr  bx-keyboard'", link: `../view_all_products_page/all_products.html?category=${encodeURIComponent('Keyboard')}` }
  ];

  const categoryContainer = document.getElementById("category-container");
  categoryContainer.innerHTML = "";

  categories.forEach(cat => {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "categoryBrowse";

    categoryDiv.innerHTML = `
      <a href="${cat.link}">
        <div class="category-name">${cat.name}</div>
        <div class="category-image"><i class='${cat.icon}'></i></div>
      </a>
    `;
    categoryContainer.appendChild(categoryDiv);
  });
}

function attachScroll(containerId, leftBtnSelector, rightBtnSelector, scrollAmount = 300) {
  const container = document.getElementById(containerId);
  const leftBtn = document.querySelector(leftBtnSelector);
  const rightBtn = document.querySelector(rightBtnSelector);

  if (!container || !leftBtn || !rightBtn) return;

  leftBtn.addEventListener("click", () => {
    container.scrollLeft -= scrollAmount;
  });

  rightBtn.addEventListener("click", () => {
    container.scrollLeft += scrollAmount;
  });
}