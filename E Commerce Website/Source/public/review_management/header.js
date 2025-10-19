//Thông tin admin đang đăng nhập
document.addEventListener("DOMContentLoaded", function () {
  const adminData = localStorage.getItem("admin");

  // Nếu không có admin => Chuyển về trang đăng nhập
  if (!adminData) {
    window.location.href = "/login_admin/login.html";
    return; // Dừng script tại đây
  }

  const admin = JSON.parse(adminData);

  // Gán tên người dùng
  const nameElement = document.getElementById("user-name");
  if (nameElement) {
    nameElement.textContent = admin.name || "Quản trị viên";
  }

  // Đăng xuất
  const logoutBtn = document.getElementById("logout-link");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", function () {
      localStorage.removeItem("admin");
      window.location.href = "/login_admin/login.html";
    });
  }
});

// Ngăn việc quay lại trang sau khi đã đăng xuất (Back button)
window.addEventListener("pageshow", function (event) {
  const adminData = localStorage.getItem("admin");
  if (!adminData) {
    window.location.href = "/login_admin/login.html";
  }
});