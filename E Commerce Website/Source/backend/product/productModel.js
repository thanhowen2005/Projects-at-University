const mongoose = require('mongoose')

const productSchema = new mongoose.Schema({
  name: { type: String, required: true },
  price: { type: Number, default: 0 }, 
  category: { type: String, required: true },

  specs: { type: [String], default: [] },         
  highlights: { type: [String], default: [] },     
  description: { type: String },

  images: { type: [String], default: [] },        
  stock: { type: Number, default: 0 },
  discount: {type: Number, default: 0},
  date: { type: String },
  sold: {type: Number},
  
});

const productModel = new mongoose.model('product', productSchema)
module.exports = productModel
