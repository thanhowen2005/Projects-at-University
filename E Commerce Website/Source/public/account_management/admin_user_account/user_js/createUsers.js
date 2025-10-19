document.getElementById("createButton").addEventListener("click", async (e) => {
    e.preventDefault();

    let role = document.getElementById("role").value.trim();
    if (role === "user") role = "user";
    else if (role === "product-admin") role = "p_admin";
    else if (role === "account-admin") role = "a_admin";

    // Lấy dữ liệu từ input
    const newUser = {
        name: document.getElementById("fullName").value.trim(),
        email: document.getElementById("email").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        address: document.getElementById("address").value.trim(),
        password: document.getElementById("password").value.trim(),
        role: role
    };

    // Kiểm tra dữ liệu
    if (!newUser.name || !newUser.email || !newUser.phone || !newUser.password) {
        alert("❌ Vui lòng điền đầy đủ các trường bắt buộc.");
        return;
    }

    try {
        const res = await fetch("http://localhost:3000/users", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newUser)
        });

        const result = await res.json();

        if (res.ok) {
            alert("✅ Tạo tài khoản thành công!");
            window.location.href = "user_account_management.html";
        } else {
            alert("❌ Lỗi tạo tài khoản: " + (result.error || result.message));
        }

    } catch (err) {
        console.error("❌ Lỗi tạo tài khoản:", err);
        alert("❌ Lỗi khi gửi yêu cầu đến server.");
    }
});
