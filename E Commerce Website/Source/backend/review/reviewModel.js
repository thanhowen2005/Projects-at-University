const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
  productid: { type: String, required: true }, 
  userid: { type: String, required: true },
  rating: { type: Number, required: true, min: 1, max: 5 },
  cmt: { type: String },
  date: { type: String, required: true },
  status: { type: Number, min: 0, max: 1 },
});

const reviewModel = mongoose.model('review', reviewSchema);
module.exports = reviewModel;