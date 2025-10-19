document.addEventListener("DOMContentLoaded", function () {
    const roleElement = document.querySelector(".body");
    const role = roleElement.getAttribute("data-role");
    const searchInput = document.querySelector(".search_input-in-content");
    const tbody = document.querySelector(".user-table tbody");

    let allUsers = [];

    fetch("http://localhost:3000/users")
        .then(res => res.json())
        .then(users => {
            allUsers = users.filter(user => user.role === role);
            renderUsers(allUsers);
        })
        .catch(err => console.error("❌ Lỗi fetch người dùng:", err));

    searchInput.addEventListener("input", () => {
        const keyword = searchInput.value.toLowerCase().trim();

        const filtered = allUsers.filter(user =>
            user.name.toLowerCase().includes(keyword) ||
            user.phone.toLowerCase().includes(keyword)
        );

        renderUsers(filtered);
    });

    function renderUsers(users) {
        tbody.innerHTML = "";

        users.forEach((user) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${user._id}</td>
                <td>${user.name}</td>
                <td>${user.phone}</td>
                <td>${mapRole(user.role)}</td>
                <td class="Action">
                    <a href="user_account_management_profile.html?id=${user._id}" class="details-link">Chi tiết</a>
                    <i class='bx bx-trash action-icon delete-icon' data-id="${user._id}" style="cursor:pointer;"></i>
                    <a href="user_account_management_profile_edit.html?id=${user._id}">
                        <i class='bx bx-edit-alt action-icon'></i>
                    </a>
                </td>
            `;
            tbody.appendChild(row);
        });

        document.querySelectorAll(".delete-icon").forEach(icon => {
            icon.addEventListener("click", async () => {
                const userId = icon.getAttribute("data-id");
                const confirmDelete = confirm("❗Bạn có chắc chắn muốn xoá người dùng này?");
                if (!confirmDelete) return;

                try {
                    const res = await fetch(`http://localhost:3000/users/${userId}`, {
                        method: "DELETE"
                    });
                    const result = await res.json();
                    if (res.ok) {
                        alert("✅ Xoá người dùng thành công!");
                        icon.closest("tr").remove();
                    } else {
                        alert("❌ Lỗi khi xoá: " + (result.error || result.message));
                    }
                } catch (err) {
                    console.error("❌ Lỗi xoá:", err);
                    alert("❌ Có lỗi xảy ra khi xoá người dùng.");
                }
            });
        });
    }

    function mapRole(role) {
        if (role === "p_admin") return "Admin Sản phẩm";
        if (role === "a_admin") return "Admin Tài khoản";
        return "Người dùng";
    }
});
