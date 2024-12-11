const express = require('express');
const mysql = require('mysql2');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

// Initialisation de l'application Express
const app = express();
app.use(cors());
app.use(express.json());

// Configuration de Multer pour stocker les images
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(__dirname, 'uploads');
        if (!fs.existsSync(uploadPath)) {
            fs.mkdirSync(uploadPath, { recursive: true });
        }
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});
const upload = multer({ storage: storage });

// Configuration de la connexion MySQL
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '', // Remplacez par votre mot de passe MySQL
    database: 'ImageDB' // Nom de la base de données
});

db.connect((err) => {
    if (err) throw err;
    console.log('✅ Base de données connectée');
});

// Route pour uploader une image
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('❌ Aucun fichier téléchargé.');
    }

    const { filename } = req.file;
    const filePath = `/uploads/${filename}`;
    const date_uploaded = new Date().toISOString();

    const query = 'INSERT INTO image (image_name, image_path, date_uploaded) VALUES (?, ?, ?)';
    db.query(query, [filename, filePath, date_uploaded], (err, result) => {
        if (err) {
            console.error('❌ Erreur lors de l\'insertion de l\'image dans la base de données', err);
            return res.status(500).send('❌ Erreur lors de l\'upload de l\'image.');
        }
        res.status(200).send({
            message: '✅ Image téléchargée avec succès',
            id: result.insertId,
            imagePath: filePath
        });
    });
});

// Route pour lister toutes les images
app.get('/images', (req, res) => {
    const query = 'SELECT id, image_name, image_path, date_uploaded FROM image';
    db.query(query, (err, results) => {
        if (err) {
            console.error('❌ Erreur lors de la récupération des images', err);
            return res.status(500).send('❌ Erreur lors de la récupération des images.');
        }
        res.status(200).json(results);
    });
});

// Route pour récupérer une image par ID
app.get('/image/:id', (req, res) => {
    const { id } = req.params;
    const query = 'SELECT image_path FROM image WHERE id = ?';
    db.query(query, [id], (err, results) => {
        if (err || results.length === 0) {
            console.error('❌ Erreur lors de la récupération de l\'image', err);
            return res.status(404).send('❌ Image introuvable.');
        }
        const imagePath = path.join(__dirname, results[0].image_path);
        res.sendFile(imagePath);
    });
});

// Lancement de l'application
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`🚀 Serveur démarré sur http://localhost:${PORT}`);
});
