import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [images, setImages] = useState([]);
  const [currentView, setCurrentView] = useState("menu"); // menu, images, upload, signals
  const [selectedImage, setSelectedImage] = useState(null); // Image actuellement sélectionnée pour le mode "Voir"
  const [signalStatus, setSignalStatus] = useState(""); // Statut des signaux

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

  // Fonction pour envoyer un signal
  const handleSignal = (signalType) => {
    axios
      .post(`http://localhost:5000/signal/${signalType}`)
      .then((response) => {
        setSignalStatus(response.data.message); // Afficher le message de statut du signal
      })
      .catch((error) => {
        console.error("Erreur lors de l'envoi du signal :", error);
        setSignalStatus("Erreur lors de l'envoi du signal.");
      });
  };

  return (
    <div className="App">
      {currentView === "menu" && (
        <div className="menu">
          <h1>Gestion des images</h1>
          <button onClick={() => setCurrentView("images")}>
            Voir les Images
          </button>
          <button onClick={() => setCurrentView("upload")}>
            Uploader une image
          </button>
          <button onClick={() => setCurrentView("signals")}>
            Signaux
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

      {currentView === "signals" && (
        <div>
          <button
            onClick={() => setCurrentView("menu")}
            className="back-button"
          >
            Retour au menu
          </button>
          <h2>Envoyer un signal</h2>
          <button
            onClick={() => handleSignal("start")}
            className="signal-button"
          >
            Démarrer
          </button>
          <button
            onClick={() => handleSignal("pause")}
            className="signal-button"
          >
            Pause
          </button>
          <button
            onClick={() => handleSignal("cancel")}
            className="signal-button"
          >
            Annuler
          </button>
          <button
            onClick={() => handleSignal("bip")}
            className="signal-button"
          >
            Bip
          </button>
          <button
            onClick={() => handleSignal("resume")}
            className="signal-button"
          >
            Reprendre
          </button>
          <p>Status du signal : {signalStatus}</p>
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
