document.addEventListener("DOMContentLoaded", () => {
    const saveButton = document.getElementById("saveButton");

    saveButton.addEventListener("click", async (e) => {
        e.preventDefault();

        const params = new URLSearchParams(window.location.search);
        const userId = params.get("id");

        if (!userId) {
            alert("❌ Không tìm thấy ID người dùng trong URL");
            return;
        }

        let role = document.getElementById("role").value.trim();
        if (role === "user") role = "user";
        else if (role === "product-admin") role = "p_admin";
        else if (role === "account-admin") role = "a_admin";

        const updatedUser = {
            name: document.getElementById("fullName").value.trim(),
            email: document.getElementById("email").value.trim(),
            phone: document.getElementById("phone").value.trim(),
            address: document.getElementById("address").value.trim(),
            password: document.getElementById("password").value.trim(),
            role: role
        };

        if (!updatedUser.email || !updatedUser.phone || !updatedUser.password || !updatedUser.role) {
            alert("❌ Vui lòng điền đầy đủ tất cả các trường trước khi lưu.");
            return;
        }
        try {
            const response = await fetch(`http://localhost:3000/users/${userId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(updatedUser)
            });

            const result = await response.json();

            if (response.ok) {
                alert("✅ Cập nhật người dùng thành công!");
                window.location.href = "user_account_management.html";
            } else {
                alert(`❌ Lỗi khi cập nhật: ${result.error || result.message || "Không xác định"}`);
            }
        } catch (err) {
            console.error("❌ Lỗi fetch:", err);
            alert("❌ Có lỗi khi gửi yêu cầu đến server.");
        }
    });
});
