document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll('.opt-field input');
    const submitBtn = document.querySelector('.btn-submit');
    const email = localStorage.getItem("resetEmail"); // Cập nhật cho khớp với forgotpassword.js
    const h3Element = document.querySelector("h3");

    // ✅ Hiển thị email
    if (email && h3Element) {
        h3Element.textContent = `Check your email: ${email}`;
    }

    // ✅ Tự chuyển con trỏ khi nhập từng ký tự
    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    // ✅ Gửi mã khôi phục để xác minh
    submitBtn.addEventListener("click", async () => {
        const code = [...inputs].map(input => input.value.trim()).join("");

        if (code.length !== 4) {
            alert("Vui lòng nhập đầy đủ 4 ký tự mã.");
            return;
        }

        try {
            const response = await fetch("http://localhost:3000/verify-reset-code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, code })
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = "/User/authentication/enter_new_password/enter_new_password.html";
            } else {
                alert("Mã không chính xác. Vui lòng thử lại.");
                document.querySelector(".opt-field").classList.add("error");
            }
        } catch (err) {
            console.error("Verification error:", err);
            alert("Có lỗi xảy ra. Vui lòng thử lại sau.");
        }
    });
});
