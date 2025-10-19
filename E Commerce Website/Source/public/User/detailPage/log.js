localStorage.setItem('user', '');

window.addEventListener('DOMContentLoaded', () => {
  const userData = localStorage.getItem('user');
  const accountElement = document.querySelector('.account');
  const signUpElement = document.querySelector('.signup');
  const userNameHeading = document.querySelector('.user-info h2');

  if (!userData || userData === '' || userData === '{}' || userData === 'null') {
    // Chưa đăng nhập -> ẩn icon person
    if (accountElement) accountElement.style.display = 'none';
    // Giữ nguyên nút Sign Up
    if (signUpElement) signUpElement.style.display = 'block';
  } else {
    // Đã đăng nhập -> ẩn nút Sign Up
    if (signUpElement) signUpElement.style.display = 'none';

    // Hiện icon person (nếu bị ẩn)
    if (accountElement) accountElement.style.display = 'flex';

    // Đổi tên người dùng
    const user = JSON.parse(userData);
    if (userNameHeading) userNameHeading.textContent = user.name || 'User';
  }
});