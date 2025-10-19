const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
    name: String,
    email: String,
    phone: String,
    password: String,
    address: String,
    role: String,
});

module.exports = mongoose.model("users", UserSchema);
