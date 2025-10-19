const mongoose = require("mongoose");

const couponSchema = new mongoose.Schema({
  percent: { type: Number, required: true, min: 1, max: 100 },
  code: { type: String, required: true, unique: true },
}, { timestamps: true });

module.exports = mongoose.model("coupon", couponSchema);