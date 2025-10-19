let cart = null;
let products = [];

const itemList = document.querySelector(".item-list");
const totalAmount = document.querySelector("#total");

// Hàm định dạng tiền VND
function formatCurrency(amount) {
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
  }).format(amount);
}

// Lấy giỏ hàng từ localStorage
function loadCartFromStorage() {
  const cartData = JSON.parse(localStorage.getItem("cart"));
  if (!cartData || !Array.isArray(cartData.items)) {
    cart = { items: [] };
  } else {
    cart = cartData;
  }
}

// Lưu giỏ hàng vào localStorage
function saveCartToStorage() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

// Tìm sản phẩm theo ID
function findProductById(id) {
  return products.find((p) => p._id === id);
}

// Hiển thị giỏ hàng
function renderCart() {
  itemList.innerHTML = "";



  if (cart.items.length === 0) {
    const totalPriceEl = document.querySelector(".total-price");
    const buyButtonEl = document.querySelector(".buy-button");
    itemList.innerHTML = `<p class="empty-cart">Chưa có sản phẩm nào trong giỏ hàng.</p>`;

    totalPriceEl.style.display = "none";
    buyButtonEl.style.display = "none";

    updateBodyHeight();
    return;
  }
  cart.items.forEach((cartItem, index) => {
    const product = findProductById(cartItem.id);
    if (!product) return;

    const finalPrice = product.discount && product.discount > 0
      ? Math.round(product.price * (1 - product.discount / 100))
      : product.price;

    const item = document.createElement("div");
    item.classList.add("cart-item");
    item.dataset.index = index;

    item.innerHTML = `
      <img src="${product.images[0]}" alt="${product.name}" class="product-image" />
      <div class="product-info">
        <h2>${product.name}</h2>
      </div>
      <div class="quantity-control">
        <button class="qty-btn minus">−</button>
        <span class="quantity">${cartItem.quantity}</span>
        <button class="qty-btn plus">+</button>
      </div>
      <div class="price">${formatCurrency(finalPrice)}</div>
      <button class="delete-btn">🗑️</button>
    `;

    itemList.appendChild(item);
  });

  updateTotal();
  saveCartToStorage(); // Lưu lại sau mỗi lần render
}

// Tính tổng tiền
function updateTotal() {
  let total = 0;

  cart.items.forEach((cartItem) => {
    const product = findProductById(cartItem.id);
    if (product) {
      const finalPrice = product.discount && product.discount > 0
        ? Math.round(product.price * (1 - product.discount / 100))
        : product.price;

      total += finalPrice * cartItem.quantity;
    }
  });

  totalAmount.textContent = formatCurrency(total);
}

itemList.addEventListener("click", async (e) => {
  const cartItemEl = e.target.closest(".cart-item");
  if (!cartItemEl) return;

  const index = parseInt(cartItemEl.dataset.index);
  const cartItem = cart.items[index];
  const product = findProductById(cartItem.id);
  if (!product) return;

  if (e.target.classList.contains("plus")) {
    if (cartItem.quantity < product.stock) {
      cartItem.quantity++;
    }
  } else if (e.target.classList.contains("minus")) {
    if (cartItem.quantity > 1) {
      cartItem.quantity--;
    }
  } else if (e.target.classList.contains("delete-btn")) {
    cart.items.splice(index, 1);
    
  }

  // Gọi API cập nhật cart
  try {
    saveCartToStorage();
    await updateCartOnServer(cart);
    renderCart();
  } catch (error) {
    console.error("Cập nhật giỏ hàng thất bại", error);
  }
});

async function updateCartOnServer(cart) {
  const user = JSON.parse(localStorage.getItem("user"));
  if (!user || !user.email) throw new Error("Bạn chưa đăng nhập");

  const res = await fetch(`http://localhost:3000/api/carts/${user.email}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cart),
  });

  if (!res.ok) throw new Error("Lỗi khi cập nhật giỏ hàng");
}


// Sự kiện nút mua
document.querySelector(".buy-button").addEventListener("click", (e) => {
  const btn = e.target;
  btn.classList.add("clicked");
  setTimeout(() => btn.classList.remove("clicked"), 200);

  // Bạn có thể thêm logic xử lý thanh toán tại đây
});

// Lấy sản phẩm từ API, sau đó load giỏ hàng
async function fetchProducts() {
  try {
    const res = await fetch("http://localhost:3000/api/products");
    products = await res.json();
    loadCartFromStorage();
    renderCart();
    updateBodyHeight();
  } catch (err) {
    console.error("Lỗi khi tải sản phẩm:", err);
  }
}

fetchProducts();



//////
//Cập nhật chiều dài của trang
function updateBodyHeight() {
  const container = document.querySelector('.body');
  if (!container) return;

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

  // Lấy chiều cao viewport
  const viewportHeight = window.innerHeight;

  // So sánh và lấy chiều cao lớn hơn giữa maxHeight và viewportHeight
  const finalHeight = Math.max(maxHeight, viewportHeight);

  // Cập nhật chiều cao cho container
  container.style.height = finalHeight + 50 +  'px';
}
