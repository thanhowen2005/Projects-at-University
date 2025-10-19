const express = require("express");
const router = express.Router();
const User = require("./models/user");
const ResetCode = require("./ResetCode");
const sendEmail = require("./emailService");

// Gửi mã reset
router.post("/send-reset-code", async (req, res) => {
    const { email } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: "Email not found" });

    const code = Math.random().toString(36).substring(2, 6).toUpperCase();

    await ResetCode.findOneAndUpdate(
        { email },
        { code, expiresAt: new Date(Date.now() + 10 * 60 * 1000) },
        { upsert: true }
    );

    await sendEmail(email, "Reset Code", `Your reset code is: ${code}`);
    res.status(200).json({ message: "Reset code sent" });
});

// Xác minh mã reset
router.post("/verify-reset-code", async (req, res) => {
    const { email, code } = req.body;

    const record = await ResetCode.findOne({ email });
    if (!record || record.code !== code || record.expiresAt < new Date()) {
        return res.status(400).json({ message: "Invalid or expired code" });
    }

    res.status(200).json({ message: "Code verified" });
});

// Đặt lại mật khẩu
router.post("/reset-password", async (req, res) => {
    const { email, newPassword } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: "User not found" });

    user.password = newPassword; // Thực tế nên hash trước khi lưu
    await user.save();

    await ResetCode.deleteOne({ email });

    res.status(200).json({ message: "Password reset successful" });
});

module.exports = router;
