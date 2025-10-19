// Chờ cho toàn bộ cấu trúc HTML của trang được tải xong rồi mới thực thi code
window.addEventListener('DOMContentLoaded', () => {

    // Lấy các phần tử cần thay đổi từ HTML
    const accountElement = document.querySelector('.account');
    const signUpElement = document.querySelector('.signup');
    const userNameHeading = document.querySelector('.user-info h2');
    const logoutLink = document.querySelector('#logout-link'); // Thêm ID cho nút đăng xuất

    // Hàm cập nhật giao diện header
    const updateHeaderUI = () => {
        // Lấy dữ liệu người dùng từ localStorage
        const userDataString = localStorage.getItem('user');
        let user = null;

        // Cố gắng chuyển đổi chuỗi JSON thành object
        // Dùng try...catch để tránh lỗi nếu dữ liệu trong localStorage bị hỏng
        if (userDataString && userDataString !== 'null') {
            try {
                user = JSON.parse(userDataString);
            } catch (error) {
                console.error("Lỗi phân tích dữ liệu người dùng từ localStorage:", error);
                // Nếu dữ liệu lỗi, coi như chưa đăng nhập
                localStorage.removeItem('user');
                user = null;
            }
        }
        
        // Kiểm tra xem người dùng đã đăng nhập hay chưa (user có tồn tại và có dữ liệu không)
        if (user && Object.keys(user).length > 0) {
            // ----- KHI NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP -----

            // Ẩn nút "Sign Up"
            if (signUpElement) {
                signUpElement.style.display = 'none';
            }

            // Hiển thị icon tài khoản và menu con
            if (accountElement) {
                // Sử dụng 'flex' vì phần tử cha có thể là flex container
                accountElement.style.display = 'flex'; 
            }

            // Cập nhật tên người dùng trong menu
            if (userNameHeading) {
                // Nếu có tên thì hiển thị, không thì dùng 'User' làm mặc định
                userNameHeading.textContent = user.name || 'User'; 
            }

        } else {
            // ----- KHI NGƯỜI DÙNG LÀ KHÁCH (CHƯA ĐĂNG NHẬP) -----

            // Hiển thị nút "Sign Up"
            if (signUpElement) {
                signUpElement.style.display = 'block'; // Hoặc 'flex' tùy thuộc vào CSS của bạn
            }

            // Ẩn icon tài khoản và menu con
            if (accountElement) {
                accountElement.style.display = 'none';
            }
        }
    };

    // Gắn sự kiện cho nút Đăng xuất
    if (logoutLink) {
        logoutLink.addEventListener('click', (event) => {
            event.preventDefault(); // Ngăn chặn hành vi mặc định của thẻ <a>
            
            // Xóa thông tin người dùng khỏi localStorage
            localStorage.removeItem('user');
            localStorage.removeItem('cart');
            
            // Tải lại trang để cập nhật header hoặc chuyển hướng về trang chủ
            window.location.href = '/User/authentication/login/login.html'; // Hoặc trỏ tới trang chủ của bạn
        });
    }

    // Gọi hàm để cập nhật giao diện ngay khi trang được tải
    updateHeaderUI();
});

window.addEventListener("pageshow", function (event) {
    const user = localStorage.getItem("user");

    if (!user || user === "null") {
        const accountElement = document.querySelector('.account');
        const signUpElement = document.querySelector('.signup');
        const userNameHeading = document.querySelector('.user-info h2');

        if (accountElement) accountElement.style.display = 'none';
        if (signUpElement) signUpElement.style.display = 'block';
        if (userNameHeading) userNameHeading.textContent = '';
    }
});


