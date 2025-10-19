router.put('/:id', async (req, res) => {
  try {
    const updatedProduct = await productModel.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }  // để trả về document sau khi update
    );
    if (!updatedProduct) {
      return res.status(404).json({ message: 'Product not found' });
    }
    res.json(updatedProduct);  // trả về sản phẩm đã được cập nhật
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});