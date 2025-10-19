const cartDiv = document.getElementById("cart-div");
const cartCountEl = document.querySelector(".cart-count");

function loadUserCart() {
  const cartData = JSON.parse(localStorage.getItem("cart"));
  if (!cartData || !Array.isArray(cartData.items)) {
    return { items: [] };
  }
  return cartData;
}

function updateCartCount(userCart) {
  if (!userCart || !userCart.items) {
    cartCountEl.textContent = 0;
    return;
  }
  // Số lượng item khác nhau trong giỏ hàng
  const itemCount = userCart.items.length;
  cartCountEl.textContent = itemCount;
}

cartDiv.addEventListener("click", () => {
  const user = JSON.parse(localStorage.getItem("user"));

  if (!user || Object.keys(user).length === 0) {
    // Nếu người dùng chưa đăng nhập, chuyển hướng đến trang đăng nhập
    window.location.href = "/User/authentication/login/login.html";
    return;
  }

  window.location.href = "../mycart/mycart.html";
});

const userCart = loadUserCart();
updateCartCount(userCart);


document.addEventListener("DOMContentLoaded", () => {
  const links = Array.from(document.querySelectorAll(".sub-menu-link"));
  
  // Tìm link "Chỉnh sửa hồ sơ"
  const profileLink = links.find(a => a.textContent.includes("Chỉnh sửa hồ sơ"));
  // Tìm link "Đơn hàng của bạn"
  const ordersLink = links.find(a => a.textContent.includes("Đơn hàng của bạn"));

  if (profileLink) profileLink.href = "../myprofile/MyProfile.html";
  if (ordersLink) ordersLink.href = "../myorder/MyOrder.html";
});
