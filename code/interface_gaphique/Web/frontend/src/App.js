import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [images, setImages] = useState([]);
  const [currentView, setCurrentView] = useState("menu"); // menu, images, upload
  const [selectedImage, setSelectedImage] = useState(null); // Image actuellement sélectionnée pour le mode "Voir"

  // Charger les images avec les aperçus
  useEffect(() => {
    if (currentView === "images") {
      axios
        .get("http://localhost:5000/images")
        .then(async (response) => {
          const imagePreviews = await Promise.all(
            response.data.map(async (image) => {
              const fullImageResponse = await axios.get(
                `http://localhost:5000/image/${image.id}`
              );
              return {
                ...image,
                image_data: fullImageResponse.data.image_data,
              };
            })
          );
          setImages(imagePreviews);
        })
        .catch((error) => {
          console.error("Erreur lors du chargement des images :", error);
        });
    }
  }, [currentView]);

  // Fonction pour transférer une image au bot
  const handleTransfer = (imageId) => {
    axios
      .post(`http://localhost:5000/transfer/${imageId}`)
      .then(() => {
        alert("Image transférée avec succès !");
      })
      .catch((error) => {
        console.error("Erreur lors du transfert :", error);
        alert("Erreur lors du transfert de l'image.");
      });
  };

  return (
    <div className="App">
      {currentView === "menu" && (
        <div className="menu">
          <h1>Gestion des images</h1>
          <button onClick={() => setCurrentView("images")}>
            Afficher les images
          </button>
          <button onClick={() => setCurrentView("upload")}>
            Uploader une image
          </button>
        </div>
      )}

      {currentView === "images" && (
        <div>
          <button
            onClick={() => setCurrentView("menu")}
            className="back-button"
          >
            Retour au menu
          </button>

          <div className="image-list">
            {images.map((image) => (
              <div key={image.id} className="image-item">
                <img
                  src={`data:image/jpeg;base64,${image.image_data}`}
                  alt="aperçu"
                  className="image-preview"
                />
                <p>{image.date_uploaded}</p>
                <button
                  className="transfer-button"
                  onClick={() => handleTransfer(image.id)}
                >
                  Transférer au bot
                </button>
                <button
                  className="view-button"
                  onClick={() => setSelectedImage(image)}
                >
                  Voir
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {currentView === "upload" && (
        <div>
          <button
            onClick={() => setCurrentView("menu")}
            className="back-button"
          >
            Retour au menu
          </button>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const formData = new FormData(e.target);
              axios
                .post("http://localhost:5000/upload", formData)
                .then(() => {
                  alert("Image uploadée avec succès !");
                  setCurrentView("menu");
                })
                .catch((error) => {
                  console.error("Erreur lors de l'upload :", error);
                  alert("Erreur lors de l'upload de l'image.");
                });
            }}
            className="upload-form"
          >
            <h2>Uploader une nouvelle image</h2>
            <input type="file" name="image" required />
            <button type="submit">Uploader</button>
          </form>
        </div>
      )}

      {selectedImage && (
        <div className="modal">
          <div className="modal-content">
            <button className="close-button" onClick={() => setSelectedImage(null)}>
              Fermer
            </button>
            <img
              src={`data:image/jpeg;base64,${selectedImage.image_data}`}
              alt="aperçu"
              className="modal-image"
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
