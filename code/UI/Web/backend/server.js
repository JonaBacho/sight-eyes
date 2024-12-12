const express = require('express');
const mysql = require('mysql2');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process'); // Pour interagir avec les processus système

// Initialisation de l'application Express
const app = express();
app.use(cors());
app.use(express.json());

// Configuration de Multer pour stocker les images sur le disque
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

// Fonction pour envoyer des signaux au processus principal
const sendSignal = (signal, res) => {
    const programPID = fs.readFileSync(path.join(__dirname, '../../signal-handler/program_pid.txt'), 'utf8'); // Stockez le PID du programme principal dans un fichier

    if (!programPID) {
        return res.status(500).send('❌ Impossible de trouver le PID du programme principal.');
    }

    try {
        process.kill(programPID, signal);
        console.log(`🔔 Signal "${signal}" envoyé au processus ${programPID}`);
        res.status(200).send(`✅ Signal "${signal}" envoyé.`);
    } catch (error) {
        console.error(`❌ Erreur lors de l'envoi du signal "${signal}"`, error);
        res.status(500).send(`❌ Erreur lors de l'envoi du signal "${signal}".`);
    }
};

// Route pour uploader une image
app.post('/upload', upload.single('image'), (req, res) => {
    if (!req.file) {
        return res.status(400).send('❌ Aucun fichier téléchargé.');
    }

    const { path: filePath, originalname } = req.file;
    const date_uploaded = new Date().toISOString();

    const query = 'INSERT INTO images (image_name, image_path, date_uploaded) VALUES (?, ?, ?)';
    db.query(query, [originalname, filePath, date_uploaded], (err, result) => {
        if (err) {
            console.error('❌ Erreur lors de l\'insertion de l\'image dans la base de données', err);
            return res.status(500).send('❌ Erreur lors de l\'upload de l\'image.');
        }
        res.status(200).send({ message: '✅ Image téléchargée avec succès', id: result.insertId });
    });
});

// Route pour lister toutes les images
app.get('/images', (req, res) => {
    const query = 'SELECT id, image_name, date_uploaded FROM images';
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
    const query = 'SELECT image_name, image_path, date_uploaded FROM images WHERE id = ?';
    db.query(query, [id], (err, results) => {
        if (err) {
            console.error('❌ Erreur lors de la récupération de l\'image', err);
            return res.status(500).send('❌ Erreur lors de la récupération de l\'image.');
        }
        if (results.length > 0) {
            const { image_name, image_path, date_uploaded } = results[0];
            const imageData = fs.readFileSync(image_path).toString('base64');
            res.status(200).json({ image_name, date_uploaded, image_data: imageData });
        } else {
            res.status(404).send('❌ Image non trouvée.');
        }
    });
});

// Routes pour envoyer des signaux au programme principal
app.post('/signal/start', (req, res) => sendSignal('SIGUSR1', res)); // START
app.post('/signal/pause', (req, res) => sendSignal('SIGUSR2', res)); // PAUSE
app.post('/signal/resume', (req, res) => sendSignal('SIGINT', res)); // RESUME
app.post('/signal/cancel', (req, res) => sendSignal('SIGTERM', res)); // CANCEL
app.post('/signal/bip', (req, res) => sendSignal('SIGALRM', res)); // BIP

// Démarrer le serveur
app.listen(5000, () => {
    console.log('✅ Serveur en écoute sur le port 5000');
});
