const express = require('express');
const router = express.Router();
const User = require('./models/user'); // Import model đã tạo

// Đăng ký tài khoản
router.post("/register", async (req, res) => {
    const { name, email, phone, password, address, role } = req.body;

    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ message: "Email already registered" });
    }

    const user = new User({ name, email, phone, password, address, role });
    await user.save();

    res.status(200).json({ message: "User registered successfully" });
});

module.exports = router;
