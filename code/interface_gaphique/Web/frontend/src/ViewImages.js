import React, { useState, useEffect } from 'react';
import ImageFrame from './ImageFrame';
import './ViewImages.css';  // Assurez-vous que le fichier CSS est importé correctement

function ViewImages() {
    const [images, setImages] = useState([]);
    const [isProcessing, setIsProcessing] = useState(false);

    // Fonction pour charger les images depuis le backend
    useEffect(() => {
        fetch('http://localhost:5000/images')
            .then(response => response.json())
            .then(data => setImages(data));
    }, []);

    // Fonction pour transférer l'image au bot
    const handleTransfer = (id) => {
        setIsProcessing(true);
        fetch(`http://localhost:5000/transfer/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(() => {
            setIsProcessing(false);
            alert('Image transférée avec succès!');
        })
        .catch((err) => {
            setIsProcessing(false);
            alert('Erreur lors du transfert');
        });
    };

    // Fonction pour envoyer un signal "pause"
    const handlePause = () => {
        fetch('http://localhost:5000/pause', { method: 'POST' })
            .then(() => alert('Pause envoyée'))
            .catch(() => alert('Erreur lors de l\'envoi de la pause'));
    };

    // Fonction pour envoyer un signal "stop"
    const handleStop = () => {
        fetch('http://localhost:5000/stop', { method: 'POST' })
            .then(() => alert('Stop envoyé'))
            .catch(() => alert('Erreur lors de l\'envoi du stop'));
    };

    return (
        <div className="view-images">
            <h2>Voir les Images</h2>
            <div className="images-list">
                {images.map(image => (
                    <ImageFrame key={image.id} image={image} onTransfer={handleTransfer} />
                ))}
            </div>
            <div className="control-buttons">
                <button onClick={handlePause} disabled={isProcessing}>Pause</button>
                <button onClick={handleStop} disabled={isProcessing}>Annuler</button>
            </div>
        </div>
    );
}

export default ViewImages;
