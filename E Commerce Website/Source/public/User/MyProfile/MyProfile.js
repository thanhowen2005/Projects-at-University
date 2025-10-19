document.addEventListener("DOMContentLoaded", () => {
  const user = JSON.parse(localStorage.getItem("user"));

  const originalData = { ...user };

  // Gán dữ liệu người dùng vào form
  document.getElementById("name").value = user.name;
  document.getElementById("email").value = user.email;
  document.getElementById("phone").value = user.phone;
  document.getElementById("address").value = user.address;

  // Toggle hiển thị phần đổi mật khẩu
  document.getElementById("togglePassword").addEventListener("click", (e) => {
    e.preventDefault();
    const section = document.getElementById("passwordSection");
    section.style.display = section.style.display === "none" ? "block" : "none";
  });

  // Cancel: khôi phục dữ liệu ban đầu
  document.getElementById("cancelBtn").addEventListener("click", () => {
    document.getElementById("name").value = originalData.name;
    document.getElementById("email").value = originalData.email;
    document.getElementById("phone").value = originalData.phone;
    document.getElementById("address").value = originalData.address;
    document.getElementById("currentPassword").value = "";
    document.getElementById("newPassword").value = "";
    document.getElementById("confirmPassword").value = "";
    document.getElementById("passwordSection").style.display = "none";
  });

  // Submit form để cập nhật
  document.getElementById("profileForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const updatedUser = {
      ...user,
      name: document.getElementById("name").value.trim(),
      email: document.getElementById("email").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      address: document.getElementById("address").value.trim(),
    };

    const currentPass = document.getElementById("currentPassword").value;
    const newPass = document.getElementById("newPassword").value;
    const confirmPass = document.getElementById("confirmPassword").value;

    if (currentPass || newPass || confirmPass) {
        if (!newPass)
        {
          alert("Vui lòng nhập mật khẩu mới");
          return;
        }
      if (currentPass !== user.password) {
        alert("Mật khẩu hiện tại không đúng!");
        return;
      }
      if (newPass !== confirmPass) {
        alert("Mật khẩu mới không khớp!");
        return;
      }
      updatedUser.password = newPass;
    }

    try {
      const res = await fetch(`http://localhost:3000/users/${user._id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedUser),
      });

      if (!res.ok) throw new Error("Cập nhật không thành công.");

      const newUserData = await res.json();

      localStorage.setItem("user", JSON.stringify(newUserData));
      alert("Cập nhật thông tin thành công!");
    } catch (err) {
      console.error("Lỗi khi cập nhật:", err);
      alert("Cập nhật thất bại. Vui lòng thử lại.");
    }
    window.location.href = "../MyProfile/MyProfile.html";
  });

  // Kích hoạt sidebar tab
  const path = window.location.pathname;
  if (path.includes("MyProfile.html")) {
    document.getElementById("profileLink")?.classList.add("active");
    document.getElementById("orderLink")?.classList.remove("active");
  } else if (path.includes("MyOrder.html")) {
    document.getElementById("orderLink")?.classList.add("active");
    document.getElementById("profileLink")?.classList.remove("active");
  }
});
