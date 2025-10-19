document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector(".btn-submit");


    function showError(input, message) {
        const formControl = input.parentElement;
        const small = formControl.querySelector("small");
        small.innerText = message;
        formControl.classList.add("error");
    }

    submitBtn.addEventListener("click", async (e) => {
        e.preventDefault();

        const emailInput = document.querySelector("input[type='email']");
        const email = emailInput.value.trim();

        if (!email) {
            showError(emailInput, "Vui lòng nhập email của bạn.");
            return;
        }

        try {
            const response = await fetch("http://localhost:3000/send-reset-code", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok) {
                // Lưu email vào localStorage để dùng cho bước tiếp theo
                localStorage.setItem("resetEmail", email);

                alert("Mã đặt lại mật khẩu đã được gửi đến email của bạn. Vui lòng kiểm tra hộp thư.");
                window.location.href = "/User/authentication/input_code_reset/input_code_reset.html";
            } else {
                alert(data.message || "Có lỗi xảy ra. Vui lòng thử lại sau.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Có lỗi xảy ra. Vui lòng thử lại sau.");
        }
    });
});
