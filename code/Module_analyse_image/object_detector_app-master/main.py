from utils.stream import ESP32VideoStream
import cv2

# Adresse IP et port de l'ESP32-CAM
ip = "172.17.0.2"  # Remplacez par l'adresse IP de votre ESP32-CAM
port = 81  # Port par défaut pour le streaming ESP32-CAM

# Dimensions des frames
width = 640
height = 480

# Initialisation et démarrage du flux
video_stream = ESP32VideoStream(ip, port, width, height).start()
print("Objet instancié !")

while True:
    frame = video_stream.read()
    print(frame)
    if frame is not None:
        # Affiche la frame dans une fenêtre
        cv2.imshow("ESP32-CAM Stream", frame)

    # Arrête si 'q' est pressé
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Libère les ressources
video_stream.stop()
cv2.destroyAllWindows()