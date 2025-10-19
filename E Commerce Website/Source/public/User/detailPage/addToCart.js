// Lấy các phần tử cần thiết
const btnAddToCart = document.getElementById('btn-add-to-cart');
const quantityEl = document.getElementById('quantity');
const notification = document.getElementById('notification');


async function addToCart(quantity) {
  if (!window.main_product || !window.main_product._id) {
    alert("Không tìm thấy sản phẩm hiện tại");
    return;
  }

  const user = JSON.parse(localStorage.getItem("user"));
  if (!user || !user.email) {
    alert("Bạn cần đăng nhập để thêm sản phẩm vào giỏ hàng");
    return;
  }

  const product = window.main_product;


  try {
    // Lấy giỏ hàng hiện tại
    let cartRes = await fetch(`http://localhost:3000/api/carts/${user.email}`);
    let cart;
    if (cartRes.status === 404) {
      cart = { email: user.email, items: [] };
    } else if (cartRes.ok) {
      cart = await cartRes.json();
    } else {
      alert("Lỗi khi lấy giỏ hàng");
      return;
    }

    // Kiểm tra sản phẩm đã có trong giỏ chưa
    const index = cart.items.findIndex(item => item.id === product._id);
    if (index >= 0) {
      cart.items[index].quantity += quantity;
      if (cart.items[index].quantity > main_product.stock)
          cart.items[index].quantity = main_product.stock;
    } else {
      cart.items.push({
        id: product._id,
        quantity: quantity
      });
    }

    // Cập nhật giỏ hàng lên server
    const updateRes = await fetch(`http://localhost:3000/api/carts/${user.email}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json"},
      body: JSON.stringify(cart),
    });

    if (!updateRes.ok) {
      alert("Lỗi khi cập nhật giỏ hàng");
      return;
    }

    // Lưu giỏ hàng localStorage
    localStorage.setItem("cart", JSON.stringify(cart));
    sessionStorage.setItem('showNotification', 'true');
    location.reload();
  } catch (error) {
    console.error(error);
    alert("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng");
  }
}


btnAddToCart.addEventListener('click', () => {
  let quantity = parseInt(quantityEl.textContent);
  if (isNaN(quantity) || quantity < 1) quantity = 1;

  addToCart(quantity)
    .then(() => {
    })
    .catch(err => {
      console.error(err);
      alert('Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng');
    });
});

window.addEventListener('DOMContentLoaded', () => {
  if (sessionStorage.getItem('showNotification') === 'true') {
    sessionStorage.removeItem('showNotification');
    notification.classList.add('show');
    setTimeout(() => {
      notification.classList.remove('show');
    }, 1000);
  }
});
