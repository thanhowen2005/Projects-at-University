const express = require('express');
const router = express.Router();
const Cart = require('./cartModel');

// GET /api/carts/:email - Lấy giỏ hàng theo email
router.get('/:email', async (req, res) => {
  const cart = await Cart.findOne({ email: req.params.email });
  if (!cart) return res.status(404).json({ message: 'Cart not found' });
  res.json(cart);
});

// POST /api/carts - Tạo giỏ hàng mới
router.post('/', async (req, res) => {
  const newCart = new Cart(req.body);
  const saved = await newCart.save();
  res.status(201).json(saved);
});

// PUT /api/carts/:email - Cập nhật giỏ hàng
router.put('/:email', async (req, res) => {
  const updated = await Cart.findOneAndUpdate(
    { email: req.params.email },
    req.body,
    { new: true, upsert: true }
  );
  res.json(updated);
});

// DELETE /api/carts/:email - Xoá giỏ hàng theo email
router.delete('/:email', async (req, res) => {
  await Cart.findOneAndDelete({ email: req.params.email });
  res.status(204).end();
});

module.exports = router;
