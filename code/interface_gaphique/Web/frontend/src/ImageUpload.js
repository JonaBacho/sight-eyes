import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = ({ navigateToImageList }) => {
    const [image, setImage] = useState(null);

    const handleFileChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleUpload = () => {
        const formData = new FormData();
        formData.append('image', image);

        axios.post('http://localhost:5000/upload', formData)
            .then((response) => {
                alert('Image téléchargée avec succès!');
                navigateToImageList();
            })
            .catch((error) => {
                console.error('Erreur lors de l\'upload:', error);
            });
    };

    return (
        <div>
            <h2>Uploader une image</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Télécharger</button>
        </div>
    );
};

export default ImageUpload;
