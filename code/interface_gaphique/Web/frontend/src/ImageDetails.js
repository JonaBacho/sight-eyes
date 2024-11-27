import './ImageDetails.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ImageDetails = ({ imageId }) => {
    const [image, setImage] = useState(null);

    useEffect(() => {
        if (imageId) {
            axios.get(`http://localhost:5000/image/${imageId}`)
                .then(response => {
                    setImage(response.data);
                })
                .catch(error => {
                    console.error('Erreur lors de la récupération de l\'image', error);
                });
        }
    }, [imageId]);

    if (!image) return <p>Chargement...</p>;

    return (
        <div>
            <h2>Détails de l'image</h2>
            <img src={`data:image/jpeg;base64,${image.image_data}`} alt={image.image_name} />
            
            <p>Date d'enregistrement: {image.date_uploaded}</p>
        </div>
    );
};

export default ImageDetails;
