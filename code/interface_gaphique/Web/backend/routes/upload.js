const express = require('express');
const multer = require('multer');
const Image = require('../models/Image');

const router = express.Router();

// Configuration de multer pour le stockage local
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null, Date.now() + '-' + file.originalname),
});
const upload = multer({ storage });

// Endpoint pour envoyer l'image au robot et la sauvegarder
router.post('/', upload.single('image'), async (req, res) => {
    const { objectName } = req.body;
    const image = new Image({
        filename: req.file.filename,
        objectName,
    });
    await image.save();
    res.json({ message: 'Image sauvegardée et envoyée au robot !' });
});

// Endpoint pour les suggestions d’objets récents
router.get('/recent-searches', async (req, res) => {
    const recentImages = await Image.find().sort({ dateUploaded: -1 }).limit(5);
    res.json(recentImages);
});

module.exports = router;
