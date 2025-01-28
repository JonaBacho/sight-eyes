import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!file) {
            alert('Veuillez sélectionner une image.');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await axios.post('http://localhost:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            onUploadSuccess(response.data.id);
            alert('Image téléchargée avec succès !');
        } catch (error) {
            console.error('Erreur lors de l\'upload de l\'image', error);
            alert('Erreur lors de l\'upload de l\'image');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button type="submit">Télécharger</button>
        </form>
    );
};

export default UploadForm;
