import React from 'react';
import './ImagePreviewModal.css';

const ImagePreviewModal = ({ image, onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{image.image_name}</h2>
        <img
          src={`data:image/png;base64,${image.image_data}`}
          alt={image.image_name}
        />
        <button onClick={onClose}>Fermer</button>
      </div>
    </div>
  );
};

export default ImagePreviewModal;
