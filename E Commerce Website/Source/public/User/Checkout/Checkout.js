async function loadData() {
  try {
    // Đọc user và cart từ localStorage
    const user = JSON.parse(localStorage.getItem("user"));
    const cart = JSON.parse(localStorage.getItem("cart"));
    if (!user || !cart) {
      alert("Vui lòng đăng nhập trước khi đặt hàng.");
      return;
    }
    fillUserInfo(user);
    // Fetch sản phẩm và mã giảm giá từ server
    const [productRes, couponRes] = await Promise.all([
      fetch("http://localhost:3000/api/products"),
      fetch("http://localhost:3000/api/coupons")
    ]);

    if (!productRes.ok || !couponRes.ok) throw new Error("Lỗi khi tải dữ liệu");

    const products = await productRes.json();
    const coupons = await couponRes.json();

    renderCart(cart, products, coupons);
    updateBodyHeight()
  } catch (err) {
    console.error("Lỗi khi tải dữ liệu:", err);
  }
}

// Hiện thông tin người dùng
function fillUserInfo(user) {
  if (!user) return;

  document.querySelector('input[name="firstName"]').value = user.name || "";
  document.querySelector('input[name="address"]').value = user.address || "";
  document.querySelector('input[name="phone"]').value = user.phone || "";
  document.querySelector('input[name="email"]').value = user.email || "";
}

// Hiện thông tin sản phẩm đặt hàng
function renderCart(cart, products, coupons) {
  let subtotal = 0;
  const container = document.querySelector(".product-list");
  container.innerHTML = "";

  cart.items.forEach(({ id, quantity }) => {
    const product = products.find(p => p._id === id);
    if (!product) return;

    const finalPrice = product.discount && product.discount > 0
      ? Math.round(product.price * (1 - product.discount / 100))
      : product.price;

    const item = document.createElement("div");
    item.className = "cart-item";
    item.innerHTML = `
      <img src="${product.images[0] || 'https://via.placeholder.com/60'}" alt="${product.name}" class="product-image">
      <span class="product-name">${product.name}</span>
      <span class="product-qty">x${quantity}</span>
      <span class="product-price">${finalPrice.toLocaleString()}đ</span>
    `;
    container.appendChild(item);

    subtotal += finalPrice * quantity;
  });


  document.getElementById("subtotal").textContent = `${subtotal.toLocaleString()}đ`;
  document.getElementById("total").textContent = `${subtotal.toLocaleString()}đ`;

  setupCouponHandler(subtotal, coupons);
}

function setupCouponHandler(subtotal, coupons) {
  document.getElementById("applyCoupon").addEventListener("click", () => {
    const code = document.getElementById("couponCode").value.trim();
    const message = document.getElementById("message");

    const coupon = coupons.find(c => c.code.toLowerCase() === code.toLowerCase());
    if (coupon) {
      const discount = coupon.percent;
      const discountedTotal = subtotal - (subtotal * discount / 100);
      document.getElementById("total").textContent = `${discountedTotal.toLocaleString()}đ`;

      message.textContent = `Mã "${code}" được áp dụng! Giảm ${discount}%`;
      message.className = "message success";
    } else {
      document.getElementById("total").textContent = `${subtotal.toLocaleString()}đ`;
      message.textContent = "Mã giảm giá không hợp lệ.";
      message.className = "message error";
    }
  });
}

// Cập nhật thông tin người dùng dựa trên thông tin mới
async function updateUser(userId, updatedData) {
  try {
    const res = await fetch(`http://localhost:3000/users/${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(updatedData),
    });

    if (!res.ok) throw new Error("Cập nhật thông tin thất bại");

    const data = await res.json();
    return data; // user mới sau khi cập nhật
  } catch (error) {
    console.error("Lỗi updateUser:", error);
    throw error;
  }
}

// Đặt lại giỏ hàng rỗng sau khi đặt hàng
async function resetCart(email) {
  try {
    const response = await fetch(`http://localhost:3000/api/carts/${email}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: [] }),
    });
    if (!response.ok) throw new Error("Failed to reset cart");
    const updatedCart = await response.json();
    console.log("Cart reset:", updatedCart);
    // Cập nhật localStorage
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  } catch (error) {
    console.error(error);
  }
}


// Tạo đơn hàng
async function createOrderWithShipping(shipping, cart, products, appliedCouponId = '') {
  const items = cart.items.map(cartItem => {
    const product = products.find(p => p._id === cartItem.id);
    if (!product) throw new Error(`Sản phẩm ${cartItem.id} không tồn tại`);

    const discount = product.discount || 0;
    const finalPrice = discount > 0
      ? Math.round(product.price * (1 - discount / 100))
      : product.price;

    return {
      name: product.name,
      image: product.images?.[0] || '',
      price: finalPrice,
      quantity: cartItem.quantity
    };
  });

  const now = new Date();
  const formattedDate = `${now.getDate()}/${now.getMonth() + 1}/${now.getFullYear()}`;

  const orderData = {
    shipping, //
    status: "1",
    date: formattedDate,
    items,
    couponId: appliedCouponId
  };

  const res = await fetch("http://localhost:3000/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orderData)
  });

  if (!res.ok) throw new Error("Tạo đơn hàng thất bại");
  const order = await res.json();
  console.log("Đơn hàng đã tạo:", order);
  return order;
}




// Xử lý đặt hàng
document.getElementById("placeOrder").addEventListener("click", async (e) => {
  e.preventDefault();

  const confirmOrder = confirm("Bạn có chắc chắn muốn đặt hàng không?");
  if (!confirmOrder) return;

  const form = document.getElementById("billingForm");
  const requiredInputs = form.querySelectorAll("input[required]");
  let allFilled = true;

  requiredInputs.forEach(input => {
    if (!input.value.trim()) {
      allFilled = false;
      input.style.borderColor = "red";
    } else {
      input.style.borderColor = "#ccc";
    }
  });

  const message = document.getElementById("message");
  if (!allFilled) {
    message.textContent = "Vui lòng điền đầy đủ thông tin bắt buộc.";
    message.className = "message error";
    return;
  }

  const user = JSON.parse(localStorage.getItem("user"));
  const cart = JSON.parse(localStorage.getItem("cart"));
  if (!user) {
    message.textContent = "Bạn cần đăng nhập để đặt hàng.";
    message.className = "message error";
    return;
  }
  if (!cart || !cart.items || cart.items.length === 0) {
    message.textContent = "Giỏ hàng trống.";
    message.className = "message error";
    return;
  }

  try {
    // Lấy lại sản phẩm để tính giá
    const productRes = await fetch("http://localhost:3000/api/products");
    if (!productRes.ok) throw new Error("Không tải được sản phẩm");
    const products = await productRes.json();

    // Lấy couponId nếu có
    const couponCode = document.getElementById("couponCode").value.trim();
    let appliedCouponId = "";
    if (couponCode) {
      const couponRes = await fetch("http://localhost:3000/api/coupons");
      const coupons = await couponRes.json();
      const coupon = coupons.find(c => c.code.toLowerCase() === couponCode.toLowerCase());
      if (coupon) {
        appliedCouponId = coupon._id;
      }
    }

    // Tạo shipping info từ form (không ghi đè vào user)
    const shippingInfo = {
      name: form.firstName.value.trim(),
      phone: form.phone.value.trim(),
      address: form.address.value.trim(),
      email: form.email.value.trim()
    };

    for (const item of cart.items) {
      const res = await fetch(`http://localhost:3000/api/products/${item.id}`);
      if (!res.ok) {
        message.textContent = `Sản phẩm ${item.id} không tồn tại hoặc đã bị xóa.`;
        message.className = "message error";
        return;
      }
      const product = await res.json();
      if ((product.stock || 0) < item.quantity) {
        message.textContent = `Sản phẩm "${product.name}" chỉ còn ${product.stock} trong kho, bạn đã chọn ${item.quantity}. Vui lòng giảm số lượng.`;
        message.className = "message error";
        return;
      }
    }
    // Tạo order (dùng shipping info thay vì userid)
    await createOrderWithShipping(shippingInfo, cart, products, appliedCouponId);


    
    // Giảm số lượng sản phẩm trong kho
    for (const item of cart.items) {
      const productId = item.id;
      const quantityToReduce = item.quantity;

      // Lấy sản phẩm hiện tại
      const res = await fetch(`http://localhost:3000/api/products/${productId}`);
      if (!res.ok) {
        console.error(`Không tìm thấy sản phẩm ${productId}`);
        continue;
      }

      const product = await res.json();
      const newStock = Math.max(0, (product.stock || 0) - quantityToReduce);
      const newSold = (product.sold || 0) + quantityToReduce;

      // Cập nhật lại sản phẩm với stock mới và sold mới
      await fetch(`http://localhost:3000/api/products/${productId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...product, stock: newStock, sold: newSold })

      });
    }

    // Reset cart
    await resetCart(user.email);

    message.textContent = "Đặt hàng thành công!";
    message.className = "message success";

    form.reset();
    document.getElementById("couponCode").value = "";

    setTimeout(() => {
      window.location.href = "http://localhost:3000/User/myorder/myorder.html";
    }, 1000);
  } catch (error) {
    console.error(error);
    message.textContent = "Có lỗi xảy ra khi xử lý đơn hàng.";
    message.className = "message error";
  }
});



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
  container.style.height = finalHeight + 'px';
}

// Gọi hàm khi trang tải xong
document.addEventListener("DOMContentLoaded", loadData);




