const inputs = document.querySelectorAll("input");
const loginBtn = document.querySelector(".btn-submit");

function showError(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector("small");
    small.innerText = message;
    formControl.classList.add("error");
}

function clearError(input) {
    const formControl = input.parentElement;
    const small = formControl.querySelector("small");
    small.innerText = "";
    formControl.classList.remove("error");
}

// Function để validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

loginBtn.addEventListener("click", async function (e) {
    e.preventDefault();

    const email = inputs[0].value.trim(); // Chỉ nhận email
    const password = inputs[1].value.trim();
    let isValid = true;

    clearError(inputs[0]);
    clearError(inputs[1]);

    // Validate email
    if (!email) {
        showError(inputs[0], "Vui lòng nhập email");
        isValid = false;
    } else if (!isValidEmail(email)) {
        showError(inputs[0], "Vui lòng nhập email hợp lệ");
        isValid = false;
    }
    
    if (!password) {
        showError(inputs[1], "Vui lòng nhập mật khẩu");
        isValid = false;
    }

    if (!isValid) return;

    try {
        const res = await fetch("http://localhost:3000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ identifier: email, password }) // Gửi email như identifier
        });

        const data = await res.json();

        if (res.ok) {
            const role = data.user.role;
            
            // Kiểm tra nếu là admin thì không cho đăng nhập ở trang user
            if (role === "a_admin" || role === "p_admin") {
                showError(inputs[0], "Tài khoản admin không thể đăng nhập tại đây. Vui lòng sử dụng trang đăng nhập admin.");
                return;
            }
            
            // Chỉ cho phép user thường đăng nhập
            if (!role || role === "user" || role === "customer") {
                // Lưu thông tin người dùng vào localStorage
                localStorage.setItem("user", JSON.stringify(data.user));
                
            
                try {
                    const cartRes = await fetch(`http://localhost:3000/api/carts/${data.user.email}`);
                    if (cartRes.ok) {
                        const cart = await cartRes.json();
                        localStorage.setItem("cart", JSON.stringify(cart));
                    } else if (cartRes.status === 404) {
                        // Nếu chưa có cart thì lưu cart trống
                        localStorage.setItem("cart", JSON.stringify({ email: data.user.email, items: [] }));
                    } else {
                        console.error('Lỗi lấy giỏ hàng');
                    }
                } catch (err) {
                    console.error('Lỗi khi gọi API giỏ hàng:', err);
                }
                window.location.href = "/User/homepage/index.html";
            } else {
                showError(inputs[1], "Bạn không có quyền truy cập trang này.");
            }

        } else {
            showError(inputs[1], data.message || "Email hoặc mật khẩu không đúng");
        }


    } catch (err) {
        alert("Lỗi kết nối máy chủ: " + err.message);
    }
});
