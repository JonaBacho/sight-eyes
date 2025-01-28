import cv2
import requests
from threading import Thread

class ESP32VideoStream:
    def __init__(self, url, width=640, height=480):
        """
        Initialise le flux vidéo depuis l'ESP32-CAM.

        :param url: URL de base de l'ESP32-CAM (exemple : http://192.168.1.1).
        :param width: Largeur des frames.
        :param height: Hauteur des frames.
        """
        self.url = url
        self.stream_url = f"{url}:81/stream"
        self.stream = cv2.VideoCapture(self.stream_url)

        # Configuration initiale
        self.width = width
        self.height = height
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.thread = None

        self.stopped = False
        self.grabbed, self.frame = self.stream.read()

        if not self.stream.isOpened():
            raise Exception(f"Impossible de se connecter à l'ESP32-CAM à l'adresse : {self.stream_url}")

    def start(self):
        """
        Démarre un thread séparé pour lire les frames en continu.
        """
        self.thread = Thread(target=self.update, args=()).start()
        return self.thread

    def update(self):
        """
        Lis les frames en continu depuis le flux vidéo.
        """
        while True:
            if self.stopped:
                return
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        """
        Retourne la dernière frame capturée.
        """
        return self.frame

    def stop(self):
        """
        Arrête le thread et libère les ressources.
        """
        self.stopped = True
        self.thread.join()
        self.stream.release()

    def set_resolution(self, index):
        """
        Change la résolution du flux vidéo en envoyant une commande HTTP.

        :param index: Indice de résolution (0 à 10).
        """
        resolutions = {
            10: "UXGA (1600x1200)",
            9: "SXGA (1280x1024)",
            8: "XGA (1024x768)",
            7: "SVGA (800x600)",
            6: "VGA (640x480)",
            5: "CIF (400x296)",
            4: "QVGA (320x240)",
            3: "HQVGA (240x176)",
            0: "QQVGA (160x120)",
        }
        try:
            if index in resolutions:
                requests.get(f"{self.url}/control?var=framesize&val={index}")
                print(f"Résolution réglée sur : {resolutions[index]}")
            else:
                print("Indice de résolution invalide.")
        except requests.RequestException:
            print("Erreur lors du changement de résolution.")

    def set_quality(self, value):
        """
        Change la qualité du flux vidéo en envoyant une commande HTTP.

        :param value: Qualité (entre 10 et 63).
        """
        try:
            if 10 <= value <= 63:
                requests.get(f"{self.url}/control?var=quality&val={value}")
                print(f"Qualité réglée sur : {value}")
            else:
                print("La valeur de qualité doit être entre 10 et 63.")
        except requests.RequestException:
            print("Erreur lors du changement de qualité.")

    def toggle_awb(self, awb):
        """
        Active ou désactive le réglage automatique de la balance des blancs (AWB).

        :param awb: Activer ou désactiver AWB (booléen).
        :return: Nouvelle valeur de AWB.
        """
        try:
            new_awb = 1 if not awb else 0
            requests.get(f"{self.url}/control?var=awb&val={new_awb}")
            print(f"AWB réglé sur : {'Activé' if new_awb else 'Désactivé'}")
            return not awb
        except requests.RequestException:
            print("Erreur lors du réglage de l'AWB.")
            return awb


if __name__ == "__main__":
    # Exemple d'utilisation
    url = "http://172.20.10.8"  # Remplacez par l'URL de votre ESP32-CAM
    video_stream = None

    try:
        # Initialisation et démarrage
        video_stream = ESP32VideoStream(url).start()

        AWB = True
        while True:
            frame = video_stream.read()
            if frame is not None:
                cv2.imshow("ESP32-CAM Stream", frame)

            key = cv2.waitKey(1)
            if key == ord('r'):  # Changer la résolution
                idx = int(input("Sélectionnez un indice de résolution (0 à 10) : "))
                video_stream.set_resolution(idx)
            elif key == ord('q'):  # Changer la qualité
                val = int(input("Définissez la qualité (10 à 63) : "))
                video_stream.set_quality(val)
            elif key == ord('a'):  # Basculer AWB
                AWB = video_stream.toggle_awb(AWB)
            elif key == 27:  # Quitter (touche ESC)
                break
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        if video_stream:
            video_stream.stop()
        cv2.destroyAllWindows()
