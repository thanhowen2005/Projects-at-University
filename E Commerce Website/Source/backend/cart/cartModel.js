const mongoose = require('mongoose');

const itemSchema = new mongoose.Schema({
  id: { type: String, required: true },
  quantity: { type: Number, required: true, min: 1 }
}, { _id: false });

const cartSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  items: { type: [itemSchema], default: [] }
});

module.exports = mongoose.model('Cart', cartSchema);