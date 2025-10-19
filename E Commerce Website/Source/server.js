// server.js
require('dotenv').config();
const express = require('express')
const mongoose = require('mongoose');
const cors = require("cors");
const app = express();
app.use(express.json());
app.use(cors());


const port = 3000;

const uri = 'mongodb+srv://thanhowen:jmApyPZlzuMA8ROs@cluster0.t7sfows.mongodb.net/Group10_SE'
mongoose.connect(uri)
  .then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.error('❌ MongoDB connection error:', err));


app.use(express.static('public'));
app.use('/public', express.static('public'));


///Sử dụng api cho trang quản lý sản phẩm
const productRoutes = require('./backend/product/product');
app.use('/api/products', productRoutes);



///Sử dụng api cho trang quản lý account
const signupApi = require("./backend/account/signup_api");
const loginApi = require("./backend/account/login_api");
const forgotpassworddApi = require("./backend/account/forgotpassword_api");
const resetApi = require("./backend/account/reset_api");
const getUsersApi = require("./backend/account/user_api");

const nodemailer = require("nodemailer");
const ResetCode = require("./backend/account/ResetCode");
const sendEmail = require("./backend/account/emailService");


// Sử dụng API đăng ký
app.use(signupApi); 
// Sử dụng API đăng nhập
app.use(loginApi);
// Sử dụng API quên mật khẩu
app.use(forgotpassworddApi);
// Sử dụng API nhập mã reset
app.use(resetApi);
// Sử dụng API lấy danh sách người dùng
app.use(getUsersApi);



///Sử dụng api cho trang quản lý đánh giá sản phẩm
const reviewRoutes = require('./backend/review/review');
app.use('/api/reviews', reviewRoutes);

///Sử dụng api cho trang quản lý đơn hàng
const orderRoutes = require('./backend/order/order');
app.use('/api/orders', orderRoutes);

///Sử dụng api cho trang quản lý coupon
const couponRoutes = require('./backend/coupon/coupon');
app.use('/api/coupons', couponRoutes);

///Sử dụng api cho trang quản lý cart
const cartRoutes = require('./backend/cart/cart');
app.use('/api/carts', cartRoutes);

//Khởi động server
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});
