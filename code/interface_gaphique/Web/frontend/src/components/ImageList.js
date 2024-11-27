import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ImagePreviewModal from './ImagePreviewModal';
import './ImageList.css';

const ImageList = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await axios.get('http://localhost:5000/images');
        setImages(response.data);
      } catch (error) {
        console.error('Erreur lors de la récupération des images:', error);
      }
    };
    fetchImages();
  }, []);

  const handleImageClick = (image) => {
    setSelectedImage(image);
  };

  return (
    <div className="image-list-container">
      <h2>Toutes les Images</h2>
      <div className="image-grid">
        {images.map((image) => (
          <div
            key={image.id}
            className="image-card"
            onClick={() => handleImageClick(image)}
          >
            <p>{image.image_name}</p>
          </div>
        ))}
      </div>
      {selectedImage && (
        <ImagePreviewModal
          image={selectedImage}
          onClose={() => setSelectedImage(null)}
        />
      )}
    </div>
  );
};

export default ImageList;
