document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.querySelector(".form-control input[type='password']");
    const confirmInput = document.querySelectorAll(".form-control input[type='password']")[1];
    const resetBtn = document.querySelector(".btn-submit");

    // Lấy email từ localStorage
    const email = localStorage.getItem("resetEmail");

    function showError(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector("small");
    small.innerText = message;
    formControl.classList.add("error");
}

    // Nếu không có email, quay lại bước gửi mã
    if (!email) {
        alert("Không tìm thấy email. Vui lòng quay lại bước trước.");
        window.location.href = "forgotpassword.html";
        return;
    }

    // Xử lý khi nhấn nút Reset Password
    resetBtn.addEventListener("click", async () => {
        const newPassword = passwordInput.value.trim();
        const confirmPassword = confirmInput.value.trim();

        // Kiểm tra đầu vào
        if (!newPassword || !confirmPassword) {
            showError(passwordInput, "Vui lòng nhập mật khẩu mới.");
            showError(confirmInput, "Vui lòng xác nhận mật khẩu mới.");
            return;
        }

        if (newPassword !== confirmPassword) {
            showError(confirmInput, "Mật khẩu không khớp.");
            return;
        } else {
            confirmInput.classList.remove("error");
        }

        try {
            const response = await fetch("http://localhost:3000/reset-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, newPassword })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Mật khẩu đã được đặt lại thành công.");
                localStorage.removeItem("reset_email");
                window.location.href = "/User/authentication/login/login.html";
            } else {
                alert("Không thể đặt lại mật khẩu.");
            }
        } catch (error) {
            console.error("Reset password error:", error);
            alert("Có lỗi xảy ra. Vui lòng thử lại sau.");
        }
    });
});
