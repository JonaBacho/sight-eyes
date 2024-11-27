import './ImageList.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ImageList = ({ onSelectImage }) => {
    const [images, setImages] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/images')
            .then(response => {
                setImages(response.data);
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des images', error);
            });
    }, []);

    return (
        <div>
            <h2>Liste des images</h2>
            {images.length > 0 ? (
                <ul>
                    {images.map(image => (
                        <li key={image.id}>
                            ID: {image.id} - {image.date_uploaded}
                            <button onClick={() => onSelectImage(image.id)}>Voir</button>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Aucune image disponible.</p>
            )}
        </div>
    );
};

export default ImageList;
