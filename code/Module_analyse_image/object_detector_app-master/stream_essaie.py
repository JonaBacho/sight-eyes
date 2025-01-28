import cv2

import numpy as np

import requests

from time import sleep

import logging

# Configuration du logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)



def connect_to_camera(esp32_ip, max_retries=5):

    """

    Tente de se connecter à l'ESP32-CAM avec plusieurs essais

    """

    url = f"http://{esp32_ip}:81/stream"

    for attempt in range(max_retries):

        try:

            logger.info(f"Tentative de connexion {attempt + 1}/{max_retries} à {url}")

            response = requests.get(url, stream=True, timeout=5)

            if response.status_code == 200:

                logger.info("Connexion réussie à l'ESP32-CAM")

                return response

            else:

                logger.warning(f"Tentative {attempt + 1}/{max_retries} échouée (Status code: {response.status_code})")

        except requests.exceptions.RequestException as e:

            logger.error(f"Erreur de connexion: {e}")

        sleep(2)

    raise Exception("Impossible de se connecter à l'ESP32-CAM")



def receive_video_stream(esp32_ip="192.168.1.100"):

    try:

        stream = connect_to_camera(esp32_ip)

        bytes_data = bytes()

        

        cv2.namedWindow("ESP32-CAM Stream", cv2.WINDOW_NORMAL)

        

        frame_count = 0

        while True:

            chunk = stream.raw.read(1024)

            if not chunk:

                logger.error("Pas de données reçues du flux")

                break

                

            bytes_data += chunk

            a = bytes_data.find(b'\xff\xd8')

            b = bytes_data.find(b'\xff\xd9')

            

            if a != -1 and b != -1:

                jpg = bytes_data[a:b+2]

                bytes_data = bytes_data[b+2:]

                

                # Vérification de la taille des données

                if len(jpg) > 0:

                    logger.debug(f"Taille du fragment JPEG: {len(jpg)} bytes")

                    

                    try:

                        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                        if frame is not None:

                            frame_count += 1

                            logger.debug(f"Frame {frame_count} décodée avec succès")

                            cv2.imshow("ESP32-CAM Stream", frame)

                        else:

                            logger.warning("Échec du décodage de la frame")

                    except Exception as e:

                        logger.error(f"Erreur lors du décodage de l'image: {e}")

                        # Sauvegarde des données corrompues pour analyse

                        with open(f"corrupt_frame_{frame_count}.jpg", "wb") as f:

                            f.write(jpg)

                else:

                    logger.warning("Fragment JPEG vide détecté")

                

                if cv2.waitKey(1) & 0xFF == ord('q'):

                    break

                    

    except Exception as e:
        logger.error(f"Erreur: {e}")
    finally:
        cv2.destroyAllWindows()



if __name__ == "__main__":

    # Remplacez par l'IP de votre ESP32-CAM

    ESP32_IP = "172.20.10.8"

    logger.info(f"Démarrage du script avec l'IP: {ESP32_IP}")

    receive_video_stream(ESP32_IP)