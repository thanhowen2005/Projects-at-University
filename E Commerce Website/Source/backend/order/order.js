const express = require('express');
const router = express.Router();
const orderModel = require('./orderModel');

// GET /api/orders - Lấy tất cả đơn hàng
router.get('/', async (req, res) => {
  const orders = await orderModel.find();
  res.json(orders);
});

// GET /api/orders/:id - Lấy đơn hàng theo ID
router.get('/:id', async (req, res) => {
  const order = await orderModel.findById(req.params.id);
  if (!order) return res.end();
  res.json(order);
});

// POST /api/orders - Tạo đơn hàng mới
router.post('/', async (req, res) => {
  const newOrder = new orderModel(req.body);
  const saved = await newOrder.save();
  res.status(201).json(saved);
});

// PUT /api/orders/:id - Cập nhật đơn hàng
router.put('/:id', async (req, res) => {
  const updated = await orderModel.findByIdAndUpdate(req.params.id, req.body, { new: true });
  if (!updated) return res.end();
  res.json(updated);
});

// DELETE /api/orders/:id - Xoá đơn hàng
router.delete('/:id', async (req, res) => {
  await orderModel.findByIdAndDelete(req.params.id);
  res.end();
});

module.exports = router;


// GET /api/orders/sold-products - Danh sách sản phẩm đã bán
router.get('/sold-products', async (req, res) => {
  const orders = await orderModel.find({ status: { $in: ['2', '3', '4'] } }); // lọc đơn đã xác nhận/thành công
  const productMap = new Map();

  for (const order of orders) {
    for (const item of order.items) {
      const { name, price, quantity } = item;
      if (!productMap.has(name)) {
        productMap.set(name, {
          name,
          totalQuantity: 0,
          totalRevenue: 0
        });
      }
      const productData = productMap.get(name);
      productData.totalQuantity += quantity;
      productData.totalRevenue += price * quantity;
    }
  }

  const soldProducts = Array.from(productMap.values());

  res.json(soldProducts);
});
