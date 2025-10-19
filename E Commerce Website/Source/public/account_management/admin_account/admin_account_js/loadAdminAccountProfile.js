document.addEventListener("DOMContentLoaded", async () => {
    const params = new URLSearchParams(window.location.search);
    const userId = params.get("id");

    if (!userId) {
        alert("❌ Không tìm thấy ID người dùng trong URL");
        return;
    }

    try {
        const response = await fetch(`http://localhost:3000/users/${userId}`);
        const user = await response.json();

        if (!user || user.error) {
            alert("❌ Không tìm thấy người dùng");
            return;
        }

        // Điền dữ liệu vào form
        document.getElementById("fullName").value = user.name || "";
        document.getElementById("email").value = user.email || "";
        document.getElementById("phone").value = user.phone || "";
        document.getElementById("address").value = user.address || "";
        document.getElementById("password").value = user.password || "";
        // Chuyển đổi role về định dạng hiển thị
        if (user.role === "user") {
            user.role = "Người dùng";
        } else if (user.role === "p_admin") {
            user.role = "Admin sản phẩm";
        } else if (user.role === "a_admin") {
            user.role = "Admin tài khoản";
        }
        document.getElementById("role").value = user.role || "";

    } catch (err) {
        console.error("❌ Lỗi khi tải người dùng:", err);
        alert("❌ Có lỗi khi tải thông tin người dùng.");
    }
});
