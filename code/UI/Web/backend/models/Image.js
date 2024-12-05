const mongoose = require('mongoose');

const ImageSchema = new mongoose.Schema({
    filename: { type: String, required: true },
    objectName: { type: String, required: true },
    dateUploaded: { type: Date, default: Date.now },
});

module.exports = mongoose.model('Image', ImageSchema);
