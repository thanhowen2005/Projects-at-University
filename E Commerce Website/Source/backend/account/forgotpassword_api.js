const express = require("express");
const router = express.Router();
const User = require("./models/user");       // Model người dùng
const ResetCode = require("./ResetCode");    // Model chứa mã reset
const sendEmail = require("./emailService"); // Hàm gửi email (tự bạn định nghĩa)

router.post("/send-reset-code", async (req, res) => {
    const { email } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: "Email not found" });

    const code = Math.random().toString(36).substring(2, 6).toUpperCase();

    await ResetCode.findOneAndUpdate(
        { email },
        { code, expiresAt: new Date(Date.now() + 10 * 60 * 1000) }, // mã hết hạn sau 10 phút
        { upsert: true }
    );

    await sendEmail(email, "Reset Code", `Your reset code is: ${code}`);
    res.status(200).json({ message: "Reset code sent" });
});

module.exports = router;
