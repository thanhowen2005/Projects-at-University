// Biến trạng thái toàn cục
let currentCategory = '';
let currentPriceValue = '';
let currentSort = '';
let currentBrand = '';
let currentPriceSort = '';
let allProducts = [];
let productWrapper = null;

// Hàm render sản phẩm
function renderProducts(products) {
  if (!productWrapper) return;
  productWrapper.innerHTML = '';

  products.forEach(p => {
    const discountPrice = p.price - p.price * p.discount / 100;
    const averageRating = p.rating?.length
      ? (p.rating.reduce((a, b) => a + b, 0) / p.rating.length).toFixed(1)
      : 0;
    const fullStars = Math.floor(averageRating);

    const card = document.createElement('div');
    card.className = 'product-card gear';
    card.innerHTML = `
      <a href="../detailPage/index.html?id=${p._id}" class="product-link" style="text-decoration:none; color: inherit;">
        ${p.discount > 0 ? `<div class="badge">-${Math.round(p.discount)}%</div>` : ''}
        <img src="${p.images[0]}" alt="${p.name}" />
        <h3>${p.name}</h3>
        <p class="price">
          ${p.discount > 0 ? `<span class="old-price">${p.price.toLocaleString('vi-VN')}₫</span>` : ''}
          ${Math.round(discountPrice).toLocaleString('vi-VN')}₫
        </p>
        <div class="rating">
          ${'<img src="images/star.png" width="14">'.repeat(fullStars)}
          ${'<img src="images/star-empty.png" width="14">'.repeat(5 - fullStars)}
          <span class="rating-count">(${p.rating?.length || 0})</span>
        </div>
      </a>
    `;
    productWrapper.appendChild(card);
  });

  updateBodyHeight();
}

// Lọc và sắp xếp sản phẩm
function applyAllFilters() {
  let result = [...allProducts];

  if (currentCategory === 'flash-sales') {
    result = result.filter(p => {
      const discount = p.discount || 0;
      const category = p.category?.toLowerCase();

      if (category === 'laptop' || category === 'laptopgaming') {
        return discount > 20;
      }
      if (category === 'mouse' || category === 'keyboard') {
        return discount > 30;
      }
      return false;
    });
  } else if (currentCategory) {
    result = result.filter(p => p.category?.toLowerCase() === currentCategory);
  }

  if (currentBrand && currentBrand !== 'all') {
    result = result.filter(p => p.specs[0].toLowerCase() == currentBrand);
  }

  if (currentPriceValue) {
    result = result.filter(p => {
      const priceAfterDiscount = p.price - (p.price * p.discount / 100);
      switch (currentPriceValue) {
        case '<1': return priceAfterDiscount < 1_000_000;
        case '1-3': return priceAfterDiscount >= 1_000_000 && priceAfterDiscount <= 3_000_000;
        case '3+': return priceAfterDiscount > 3_000_000;
        case '10-20': return priceAfterDiscount >= 10_000_000 && priceAfterDiscount <= 20_000_000;
        case '20-30': return priceAfterDiscount > 20_000_000 && priceAfterDiscount <= 30_000_000;
        case '30+': return priceAfterDiscount > 30_000_000;
        default: return true;
      }
    });
  }

  if (currentPriceSort === 'Thấp-Cao') {
    result.sort((a, b) =>
      (a.price - a.price * a.discount / 100) - (b.price - b.price * b.discount / 100));
  } else if (currentPriceSort === 'Cao-Thấp') {
    result.sort((a, b) =>
      (b.price - b.price * b.discount / 100) - (a.price - a.price * a.discount / 100));
  }

  switch (currentSort) {
    case 'A-Z': result.sort((a, b) => a.name.localeCompare(b.name)); break;
    case 'Z-A': result.sort((a, b) => b.name.localeCompare(a.name)); break;
    case 'Mới nhất': result.sort((a, b) => new Date(b.date) - new Date(a.date)); break;
    case 'Bán chạy': result.sort((a, b) => b.sold - a.sold); break;
  }

  renderProducts(result);
}

// Gắn rating vào từng sản phẩm
function attachRatingsToProducts(products, reviews) {
  const confirmedReviews = reviews.filter(r => r.status === 1);
  return products.map(product => {
    const ratings = confirmedReviews
      .filter(r => r.productid === product.id || r.productid === product._id)
      .map(r => r.rating);
    return { ...product, rating: ratings };
  });
}

// Hiển thị bộ lọc theo thương hiệu
function updateBrandFilterVisibilityByCategory() {
  const brandLaptop = document.getElementById('filter-brand-laptop');
  const brandMouse = document.getElementById('filter-brand-mouse');
  const brandKeyboard = document.getElementById('filter-brand-keyboard');

  // Ẩn toàn bộ dropdown brand trước
  [brandLaptop, brandMouse, brandKeyboard].forEach(el => {
    if (el) {
      el.style.display = 'none';
    }
  });

  // Nếu không có lọc theo giá -> cũng không hiển thị dropdown
  if (!currentPriceValue && !currentCategory) return;

  // Hiển thị dropdown theo category nếu đang lọc theo giá (nhưng không brand)
  if ((currentCategory === 'laptop' || currentCategory === 'laptopgaming') && brandLaptop) {
    brandLaptop.style.display = 'inline-block';
  } else if (currentCategory === 'mouse' && brandMouse) {
    brandMouse.style.display = 'inline-block';
  } else if (currentCategory === 'keyboard' && brandKeyboard) {
    brandKeyboard.style.display = 'inline-block';
  }
}

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

// Sự kiện DOMContentLoaded
document.addEventListener('DOMContentLoaded', async () => {
  productWrapper = document.querySelector('.product-slide');

  try {
    const resProducts = await fetch('http://localhost:3000/api/products');
    const products = await resProducts.json();

    const resReviews = await fetch('http://localhost:3000/api/reviews');
    const reviews = await resReviews.json();

    allProducts = attachRatingsToProducts(products, reviews);

    const params = new URLSearchParams(window.location.search);
    currentCategory = params.get('category')?.toLowerCase() || '';
    currentBrand = params.get('brand')?.toLowerCase() || '';
    currentPriceValue = params.get('price') || '';

    applyAllFilters();
    updateBrandFilterVisibilityByCategory();

    // --- Dropdown chọn brand theo từng loại ---
    document.getElementById('filter-brand-laptop')?.addEventListener('change', (e) => {
      currentBrand = e.target.value.toLowerCase();
      applyAllFilters();
      updateBrandFilterVisibilityByCategory();
    });

    document.getElementById('filter-brand-mouse')?.addEventListener('change', (e) => {
      currentBrand = e.target.value.toLowerCase();
      applyAllFilters();
      updateBrandFilterVisibilityByCategory();
    });

    document.getElementById('filter-brand-keyboard')?.addEventListener('change', (e) => {
      currentBrand = e.target.value.toLowerCase();
      applyAllFilters();
      updateBrandFilterVisibilityByCategory();
    });

    // --- Dropdown lọc theo mức giá ---
    document.getElementById('filter-price')?.addEventListener('change', e => {
      currentPriceSort = e.target.value;
      applyAllFilters();
      updateBrandFilterVisibilityByCategory();
    });

    // --- Toggle hiển thị menu sắp xếp ---
    const filterToggle = document.querySelector('.filter-toggle');
    const sortMenu = document.querySelector('.sort-menu');

    filterToggle?.addEventListener('click', () => {
      sortMenu.style.display = sortMenu.style.display === 'block' ? 'none' : 'block';
    });

    sortMenu?.addEventListener('click', (e) => {
      const sort = e.target.getAttribute('data-sort');
      if (sort) {
        currentSort = sort;
        sortMenu.style.display = 'none';
        applyAllFilters();
      }
    });

    // --- Ẩn menu sắp xếp khi click ra ngoài ---
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.sort-filter-container')) {
        sortMenu.style.display = 'none';
      }
    });

  } catch (err) {
    console.error('Lỗi khi tải dữ liệu:', err);
    renderProducts(allProducts);
  }
});
