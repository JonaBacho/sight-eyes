const express = require('express');
const mysql = require('mysql2');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios'); // Pour envoyer des requêtes HTTP
const path = require('path');

// Initialisation de l'application Express
const app = express();
app.use(cors());
app.use(express.json());

// Configuration de Multer pour stocker les images en mémoire
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Configuration de la connexion MySQL
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'ImageDB'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Base de données connectée');
});

// Adresse de l'ESP32-CAM (remplacez par votre adresse IP ESP32 réelle)
const ESP32_URL = 'http://192.168.1.100'; // Exemple : 192.168.1.100

// Route pour uploader l'image
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('Aucun fichier téléchargé');
    }

    const { buffer, originalname } = req.file;
    const date_uploaded = new Date().toISOString();

    const query = 'INSERT INTO images (image_name, image_data, date_uploaded) VALUES (?, ?, ?)';
    db.query(query, [originalname, buffer, date_uploaded], (err, result) => {
        if (err) {
            console.error('Erreur lors de l\'insertion de l\'image', err);
            return res.status(500).send('Erreur lors de l\'upload de l\'image');
        }
        res.status(200).send({ message: 'Image téléchargée avec succès', id: result.insertId });
    });
});

// Route pour lister les images
app.get('/images', (req, res) => {
    const query = 'SELECT id, image_name, date_uploaded FROM images';
    db.query(query, (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération des images', err);
            return res.status(500).send('Erreur lors de la récupération des images');
        }
        res.status(200).json(results);
    });
});

// Route pour récupérer une image par ID
app.get('/image/:id', (req, res) => {
    const { id } = req.params;
    const query = 'SELECT id, image_name, image_data, date_uploaded FROM images WHERE id = ?';
    db.query(query, [id], (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération de l\'image', err);
            return res.status(500).send('Erreur lors de la récupération de l\'image');
        }
        if (results.length > 0) {
            const { image_data, image_name, date_uploaded } = results[0];
            res.status(200).json({ image_data: image_data.toString('base64'), image_name, date_uploaded });
        } else {
            res.status(404).send('Image non trouvée');
        }
    });
});

// Route pour transférer une image et envoyer le signal "start"
app.post('/transfer/:id', async (req, res) => {
    const { id } = req.params;

    const query = 'SELECT image_data FROM images WHERE id = ?';
    db.query(query, [id], async (err, results) => {
        if (err) {
            console.error('Erreur lors de la récupération de l\'image', err);
            return res.status(500).send('Erreur lors du transfert de l\'image');
        }

        if (results.length > 0) {
            const { image_data } = results[0];
            try {
                // Envoyer l'image à l'ESP32-CAM
                await axios.post(`${ESP32_URL}/upload`, {
                    image: image_data.toString('base64'),
                });

                // Envoyer le signal "start"
                await axios.post(`${ESP32_URL}/control`, { signal: 'start' });

                res.status(200).send('Image transférée et signal "start" envoyé');
            } catch (error) {
                console.error('Erreur lors de la communication avec l\'ESP32', error);
                res.status(500).send('Erreur lors du transfert ou du signal "start"');
            }
        } else {
            res.status(404).send('Image non trouvée');
        }
    });
});

// Route pour envoyer le signal "pause"
app.post('/pause', async (req, res) => {
    try {
        await axios.post(`${ESP32_URL}/control`, { signal: 'pause' });
        res.status(200).send('Signal "pause" envoyé');
    } catch (error) {
        console.error('Erreur lors de l\'envoi du signal "pause"', error);
        res.status(500).send('Erreur lors de l\'envoi du signal "pause"');
    }
});

// Route pour envoyer le signal "stop"
app.post('/stop', async (req, res) => {
    try {
        await axios.post(`${ESP32_URL}/control`, { signal: 'stop' });
        res.status(200).send('Signal "stop" envoyé');
    } catch (error) {
        console.error('Erreur lors de l\'envoi du signal "stop"', error);
        res.status(500).send('Erreur lors de l\'envoi du signal "stop"');
    }
});

// Lancer le serveur
app.listen(5000, () => {
    console.log('Serveur en écoute sur le port 5000');
});
