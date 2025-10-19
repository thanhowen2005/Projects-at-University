// api/users_api.js
const express = require("express");
const router = express.Router();
const User = require("./models/user"); // chỉnh path nếu cần

// GET all users
router.get("/users", async (req, res) => {
  try {
    const users = await User.find(); // lấy hết users
    res.json(users);
  } catch (err) {
    res.status(500).json({ message: "Lỗi server", error: err.message });
  }
});

// GET user based on id:
router.get("/users/:id", async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) return res.status(404).json({ message: "User not found" });
    res.json(user);
  } catch (err) {
    res.status(500).json({ message: "Lỗi server", error: err.message });
  }
});

// PUT update user
router.put("/users/:id", async (req, res) => {
  try {
    const userId = req.params.id;
    const existingUser = await User.findOne({ email: req.body.email });

    // Nếu email đã tồn tại và thuộc về user khác
    if (existingUser && existingUser._id.toString() !== userId) {
      return res.status(400).json({ error: "Email đã tồn tại. Vui lòng dùng email khác." });
    }

    const updatedUser = await User.findByIdAndUpdate(userId, req.body, { new: true });

    if (!updatedUser) {
      return res.status(404).json({ message: "User not found" });
    }

    res.json(updatedUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /users – Tạo user mới
router.post("/users", async (req, res) => {
  try {
    const existingUser = await User.findOne({ email: req.body.email });
    if (existingUser) {
      return res.status(400).json({ error: "Email đã tồn tại. Vui lòng dùng email khác." });
    }

    const newUser = new User(req.body);
    await newUser.save();
    res.status(201).json(newUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE user by ID
router.delete("/users/:id", async (req, res) => {
  try {
    const deletedUser = await User.findByIdAndDelete(req.params.id);
    if (!deletedUser) {
      return res.status(404).json({ message: "Không tìm thấy người dùng để xóa" });
    }
    res.json({ message: "Đã xóa người dùng thành công", deletedUser });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


module.exports = router;