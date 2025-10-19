const mongoose = require('mongoose');

// Item schema 
const itemSchema = new mongoose.Schema({
  name: { type: String, required: true },
  image: { type: String, default: '' },
  price: { type: Number, required: true },
  quantity: { type: Number, required: true }
}, { _id: false });

// Shipping schema 
const shippingSchema = new mongoose.Schema({
  name: { type: String, required: true },
  address: { type: String, required: true },
  email: { type: String, required: true },
  phone: { type: String, required: true }
}, { _id: false });


const orderSchema = new mongoose.Schema({
  shipping: { type: shippingSchema, required: true },
  status: { type: String, default: "0" },
  date: { type: String, default: '' },
  items: { type: [itemSchema], required: true },
  couponId: { type: String, default: '' },
});

const orderModel = mongoose.model('order', orderSchema);
module.exports = orderModel;