const express = require('express');
const router = express.Router();
const reviewModel = require('./reviewModel');

// Lấy tất cả reviews
router.get('/', async (req, res) => {
  const reviews = await reviewModel.find();
  res.json(reviews);
});

// Lấy review theo id
router.get('/:id', async (req, res) => {
  try {
    const review = await reviewModel.findById(req.params.id);
    if (!review) return res.status(404).json({ message: 'Review not found' });
    res.json(review);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// Tạo review mới
router.post('/', async (req, res) => {
  try {
    const newReview = new reviewModel(req.body);
    const savedReview = await newReview.save();
    res.status(201).json(savedReview);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Cập nhật review
router.put('/:id', async (req, res) => {
  const updated = await reviewModel.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(updated);
});

// Xoá review
router.delete('/:id', async (req, res) => {
  await reviewModel.findByIdAndDelete(req.params.id);
  res.json({ message: "Review deleted" });
});

module.exports = router;
