// fproduct/product.js
const express = require('express');
const router = express.Router();
const productModel = require('./productModel');

// GET /api/products
router.get('/', async (req, res) => {
    const products = await productModel.find();
    res.json(products);
});

// GET /api/products/:id
router.get('/:id', async (req, res) => {                      
  try {
    const productId = req.params.id;                          // Lấy id sản phẩm từ URL params
    const product = await productModel.findById(productId);  // Tìm sản phẩm trong DB theo id
    if (!product) {                                           // Nếu không tìm thấy sản phẩm
      return res.status(404).json({ message: 'Product not found' }); // Trả về lỗi 404 kèm thông báo
    }
    res.json(product);                                        // Trả về dữ liệu sản phẩm dưới dạng JSON
  } catch (error) {
    res.status(500).json({ message: error.message });        // Lỗi server thì trả về mã 500 và message lỗi
  }
});


// CREATE /api/products
router.post('/', async (req, res) => {
  try {
    const newProduct = new productModel(req.body); // Tạo sản phẩm mới từ req.body
    const savedProduct = await newProduct.save();  // Lưu vào MongoDB
    res.status(201).json(savedProduct);            // Trả về sản phẩm đã tạo
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// UPDATE /api/products/:id
router.put('/:id', async (req, res) => {
  const updatedProduct = await productModel.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(updatedProduct);
});


// DELETE /api/product/:id
router.delete('/:id', async (req, res) => {
  await productModel.findByIdAndDelete(req.params.id).finally(() => res.end());
});

// GET /api/products/search/:query - Search products by name
router.get('/search/:query', async (req, res) => {
    try {
        const query = req.params.query;
        if (!query || query.trim() === '') {
            return res.status(400).json({ message: 'Search query is required' });
        }

        // Tìm kiếm sản phẩm có tên chứa từ khóa (case-insensitive)
        const products = await productModel.find({
            name: { $regex: query, $options: 'i' }
        }).limit(10); // Giới hạn 10 kết quả để làm suggestion

        res.json(products);
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
});

module.exports = router;

