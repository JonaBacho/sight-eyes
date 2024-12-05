import React, { useState, useEffect } from "react";
import axios from "axios";
import ModalViewer from "./ModalViewer";
import "./SightEyeEngine.css";

function SightEyeEngine() {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [buttonsEnabled, setButtonsEnabled] = useState(false);

  useEffect(() => {
    fetchImages();
  }, []);

  const fetchImages = async () => {
    try {
      const response = await axios.get("http://localhost:5000/images");
      setImages(response.data);
    } catch (error) {
      console.error("Erreur lors du chargement des images :", error);
    }
  };

  const handleImageClick = (image) => {
    setSelectedImage(image);
    setButtonsEnabled(true); // Activer les boutons
  };

  const handleTransfer = async (id) => {
    try {
      await axios.post(`http://localhost:5000/transfert/${id}`);
      alert("Image transférée au bot !");
    } catch (error) {
      console.error("Erreur lors du transfert :", error);
    }
  };

  const handlePause = async () => {
    try {
      await axios.post("http://localhost:5000/pause");
      alert("Signal 'pause' envoyé !");
    } catch (error) {
      console.error("Erreur lors de la pause :", error);
    }
  };

  const handleCancel = async () => {
    try {
      await axios.post("http://localhost:5000/stop");
      alert("Signal 'stop' envoyé !");
    } catch (error) {
      console.error("Erreur lors de l'arrêt :", error);
    }
  };

  return (
    <div className="sight-eye-engine">
      <h1>SightEye Research Engine</h1>

      <div className="buttons">
        <button onClick={handlePause} disabled={!buttonsEnabled}>
          Pause
        </button>
        <button onClick={handleCancel} disabled={!buttonsEnabled}>
          Cancel
        </button>
      </div>

      <div className="gallery">
        {images.map((image) => (
          <div className="image-card" key={image.id} onClick={() => handleImageClick(image)}>
            <img src={`data:image/jpeg;base64,${image.image_data}`} alt="Preview" />
            <button onClick={() => handleTransfer(image.id)}>Transfer to the Bot</button>
          </div>
        ))}
      </div>

      {selectedImage && (
        <ModalViewer
          image={selectedImage}
          onClose={() => setSelectedImage(null)}
        />
      )}
    </div>
  );
}

export default SightEyeEngine;
