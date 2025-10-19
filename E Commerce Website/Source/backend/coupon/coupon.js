const express = require("express");
const router = express.Router();
const Coupon = require("./couponModel"); 

// [POST] /api/coupons – Tạo mã giảm giá mới
router.post("/", async (req, res) => {
  try {
    const { code, percent } = req.body;

    if (!code || !percent) {
      return res.status(400).json({ error: "Thiếu thông tin mã giảm giá" });
    }

    // Kiểm tra coupon code đã tồn tại chưa
    const existed = await Coupon.findOne({ code });
    if (existed) {
      return res.status(409).json({ error: "Mã coupon đã tồn tại" });
    }

    // Tạo coupon mới
    const newCoupon = new Coupon({ code, percent });
    await newCoupon.save();

    res.status(201).json({ message: "Tạo mã giảm giá thành công", coupon: newCoupon });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
  
  // [GET] /api/coupons – Lấy toàn bộ coupon
  router.get("/", async (req, res) => {
    try {
      const coupons = await Coupon.find();
      res.json(coupons);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });
  
  // [GET] /api/coupons/:id – Lấy chi tiết 1 coupon
router.get("/:id", async (req, res) => {
  try {
    const coupon = await Coupon.findById(req.params.id).select('code percent');
    if (!coupon) {
      return res.status(404).json({ error: "Không tìm thấy coupon" });
    }
    res.json(coupon);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
  
  // [PUT] /api/coupons/:id – Cập nhật coupon
  router.put("/:id", async (req, res) => {
    try {
      const { code, percent } = req.body;
  
      if (!code || !percent) {
        return res.status(400).json({ error: "Thiếu thông tin coupon" });
      }
  
      const updatedCoupon = await Coupon.findByIdAndUpdate(
        req.params.id,
        { code, percent },
        { new: true }
      );
  
      if (!updatedCoupon) {
        return res.status(404).json({ error: "Không tìm thấy coupon để cập nhật" });
      }
  
      res.json({ message: "Cập nhật coupon thành công", coupon: updatedCoupon });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });
  
  // [DELETE] /api/coupons/:id – Xoá coupon
  router.delete("/:id", async (req, res) => {
    try {
      const deletedCoupon = await Coupon.findByIdAndDelete(req.params.id);
      if (!deletedCoupon) {
        return res.status(404).json({ error: "Không tìm thấy coupon để xoá" });
      }
      res.json({ message: "Đã xoá thành công", deletedCoupon });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });
  
  module.exports = router;