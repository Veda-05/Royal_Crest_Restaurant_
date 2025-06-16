const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    firstname: String,
    lastname: String,
    email: String,
    password: String,
    mobile: Number,
});

module.exports = mongoose.model('users', userSchema);
