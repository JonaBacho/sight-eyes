import React from 'react';
import './ImageFrame.css';  // Assurez-vous que le fichier CSS est importé correctement

function ImageFrame({ image, onTransfer }) {
    return (
        <div className="image-frame">
            <img src={`data:image/jpeg;base64,${image.image_data}`} alt={image.image_name} />
            <h3>{image.image_name}</h3>
            <button onClick={() => onTransfer(image.id)}>Transférer au bot</button>
        </div>
    );
}

export default ImageFrame;
