const mongoose = require("mongoose");

const ResetCodeSchema = new mongoose.Schema({
  email: String,
  code: String,
  expiresAt: Date
});

module.exports = mongoose.model("ResetCode", ResetCodeSchema);