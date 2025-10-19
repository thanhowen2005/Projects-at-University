// signup.js
const fullnameInput = document.querySelector('input[placeholder="Họ và tên của bạn"]');
const emailInput = document.querySelector('input[placeholder="Địa chỉ email"]');
const phoneInput = document.querySelector('input[placeholder="Số điện thoại"]');
const addressInput = document.querySelector('input[placeholder="Địa chỉ"]');
const roleInput = 'user'; 
const passwordInput = document.querySelector('input[placeholder="Mật khẩu"]');
const confirmInput = document.querySelector('input[placeholder="Xác nhận mật khẩu"]');
const submitButton = document.querySelector('.btn-submit');

function showError(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    small.innerText = message;
    formControl.classList.add('error');
    
    // Trigger animation cho container
    const container = document.querySelector('.container');
    container.style.transform = 'scale(1.02)';
    setTimeout(() => {
        container.style.transform = 'scale(1)';
    }, 300);
}

function clearError(input) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    small.innerText = '';
    formControl.classList.remove('error');
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
    // Regex cho số điện thoại Việt Nam
    return /^(\+84|84|0)[1-9][0-9]{8,9}$/.test(phone.replace(/\s+/g, ''));
}

function isValidPassword(password) {
    return password.length >= 6;
}

submitButton.addEventListener('click', function (e) {
    e.preventDefault();
    let isValid = true;

    // Clear tất cả errors trước khi validate
    [fullnameInput, emailInput, phoneInput, addressInput, passwordInput, confirmInput].forEach(input => {
        if (input) clearError(input);
    });

    // Validate fullname
    if (!fullnameInput || fullnameInput.value.trim() === '') {
        showError(fullnameInput, 'Họ và tên là bắt buộc');
        isValid = false;
    } else if (fullnameInput.value.trim().length < 2) {
        showError(fullnameInput, 'Họ và tên phải có ít nhất 2 ký tự');
        isValid = false;
    }

    // Validate email
    if (!emailInput || emailInput.value.trim() === '') {
        showError(emailInput, 'Yêu cầu nhập địa chỉ email');
        isValid = false;
    } else if (!isValidEmail(emailInput.value.trim())) {
        showError(emailInput, 'Địa chỉ email không hợp lệ');
        isValid = false;
    }

    // Validate phone
    if (!phoneInput || phoneInput.value.trim() === '') {
        showError(phoneInput, 'Yêu cầu nhập số điện thoại');
        isValid = false;
    } else if (!isValidPhone(phoneInput.value.trim())) {
        showError(phoneInput, 'Số điện thoại không hợp lệ');
        isValid = false;
    }

    // Validate address
    if (!addressInput || addressInput.value.trim() === '') {
        showError(addressInput, 'Yêu cầu nhập địa chỉ');
        isValid = false;
    } else if (addressInput.value.trim().length < 5) {
        showError(addressInput, 'Địa chỉ phải có ít nhất 5 ký tự');
        isValid = false;
    }

    // Validate password
    if (!passwordInput || passwordInput.value.trim() === '') {
        showError(passwordInput, 'Yêu cầu nhập mật khẩu');
        isValid = false;
    } else if (!isValidPassword(passwordInput.value.trim())) {
        showError(passwordInput, 'Mật khẩu phải có ít nhất 6 ký tự');
        isValid = false;
    }

    // Validate confirm password
    if (!confirmInput || confirmInput.value.trim() === '') {
        showError(confirmInput, 'Yêu cầu xác nhận mật khẩu');
        isValid = false;
    } else if (confirmInput.value.trim() !== passwordInput.value.trim()) {
        showError(confirmInput, 'Mật khẩu không khớp');
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    if (isValid) {
        fetch('http://localhost:3000/register', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: fullnameInput.value.trim(),
                email: emailInput.value.trim(),
                phone: phoneInput.value.trim(),
                address: addressInput.value.trim(),
                role: roleInput,
                password: passwordInput.value.trim()
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message); });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            // Tạo giỏ hàng rỗng cho user mới
            return fetch('http://localhost:3000/api/carts', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                email: emailInput.value.trim(),
                items: []
            })
            });
        })
        .then(data => {
            window.location.href = "/User/authentication/login/login.html";
        })
        .catch(err => {
            alert("Lỗi: " + err.message);
        });
    }
});
