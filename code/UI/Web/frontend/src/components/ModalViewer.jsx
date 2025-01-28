import React from "react";
import "./ModalViewer.css";

function ModalViewer({ image, onClose }) {
  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={onClose}>
          &times;
        </span>
        <img src={`data:image/jpeg;base64,${image.image_data}`} alt="Selected" />
      </div>
    </div>
  );
}

export default ModalViewer;
