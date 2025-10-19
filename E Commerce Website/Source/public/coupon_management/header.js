//Thông tin admin đang đăng nhập
 document.addEventListener("DOMContentLoaded", function () {
      const userData = localStorage.getItem("admin");

      // Nếu không có user => Chuyển về trang đăng nhập
      if (!userData) {
        window.location.href = "/login_admin/login.html";
        return; // Dừng script tại đây
      }


      const user = JSON.parse(userData);

      // Gán tên người dùng
      const nameElement = document.getElementById("user-name");
      if (nameElement) {
        nameElement.textContent = user.name || "Người dùng";
      }

      // Đăng xuất
      const logoutBtn = document.getElementById("logout-link");
      logoutBtn.addEventListener("click", function () {
        localStorage.removeItem("admin");
        window.location.href = "/login_admin/login.html"; // hoặc trang đăng nhập của bạn
      });

  });

// Ngăn việc quay lại trang sau khi đã đăng xuất (Back button)
window.addEventListener("pageshow", function (event) {
  const userData = localStorage.getItem("admin");
  if (!userData) {
    window.location.href = "/login_admin/login.html";
  }
});