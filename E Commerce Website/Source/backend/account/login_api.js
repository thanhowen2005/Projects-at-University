const express = require("express");
const router = express.Router();
const User = require("./models/user"); // Import model User đã định nghĩa

// Đăng nhập
router.post("/login", async (req, res) => {
    const { identifier, password } = req.body;

    try {
        const user = await User.findOne({
            $or: [{ email: identifier }, { phone: identifier }]
        });

        if (!user || user.password !== password) {
            return res.status(401).json({ message: "Vui lòng nhập chính xác thông tin tài khoản" });
        }

        res.status(200).json(
            { 
                message: "Login successful",
                user: user
            });
        
    } catch (err) {
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
