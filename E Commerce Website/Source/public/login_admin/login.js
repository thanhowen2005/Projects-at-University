const inputs = document.querySelectorAll("input");
const loginBtn = document.querySelector(".btn-submit");

loginBtn.addEventListener("click", async function (e) {
    e.preventDefault();

    const identifier = inputs[0].value.trim(); // email hoặc số điện thoại
    const password = inputs[1].value.trim();

    try {
        const res = await fetch("http://localhost:3000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ identifier, password })
        });

        const data = await res.json();
        if (res.ok) {
            const role = data.user.role;
            console.log('Role:', role);
            const userId = data.user._id;
            
            localStorage.setItem("admin", JSON.stringify(data.user));

            if (role == "a_admin") {
                window.location.href = `../account_management/admin_user_account/user_account_management.html?userId=${userId}`;
            } else if (role == "p_admin") {
                window.location.href = `../dashboard/index.html?userId=${userId}`;
            } else {
                alert("Bạn không có quyền đăng nhập trang này!");
            }
        } else {
            alert(data.message || "Đăng nhập thất bại!");
        }
    } catch (err) {
        alert("Lỗi máy chủ. Vui lòng thử lại.");
    }
});
