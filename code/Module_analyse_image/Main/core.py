import os
import numpy as np
from arduino import ArduinoCommunication
from threading import Event
from client import Client

class Core:
    def __init__(self, image_path=None, target_name=None, server_address="localhost", port="12345"):
        """
        Initialise le tracker d'objets.

        :param source: 'webcam' ou 'stream' pour choisir la source vidéo.
        :param stream_url: URL du flux vidéo en streaming (requis si source='stream').
        :param image_path: Chemin vers une image pour identifier l'objet cible.
        :param target_name: Nom de l'objet cible parmi les 90 reconnus.
        :param fov_horizontal: Champ de vision horizontal en degrés (par défaut 60 pour ESP32-cam).
        :param fov_vertical: Champ de vision vertical en degrés (par défaut 40 pour ESP32-cam).
        :param webcam_width: Largeur de la vidéo pour webcam (par défaut 640 pixels).
        :param webcam_height: Hauteur de la vidéo pour webcam (par défaut 480 pixels).
        """
        self.image_path = image_path
        self.target_name = target_name

        self.model_name = 'ssd_mobilenet_v1_coco_11_06_2017'
        self.cwd_path = os.getcwd()
        self.path_to_ckpt = os.path.join(self.cwd_path, 'object_detection', self.model_name, 'frozen_inference_graph.pb')
        self.path_to_labels = os.path.join(self.cwd_path, 'object_detection', 'data', 'mscoco_label_map.pbtxt')
        self.target_id = None
        self.current_speed = 0  # Vitesse initiale
        self.arduino_comm = ArduinoCommunication(port='LPT1', baudrate=9600)
        self.stop_event = Event()
        self.websocket_client = Client(server_address,port)

        # Identifie l'objet cible
        try:
            self.websocket_client.receive()
            if self.image_path:
                self.target_id = self._identify_target_from_image()
            elif self.target_name:
                self.target_id = self._get_target_id_by_name()
        except Exception as e:
            raise e

    def stop_tracking(self):
        self.stop_event.set()
        self.websocket_client.stop()

    def resume_tracking(self):
        self.stop_event.clear()
        
    def start_tracking(self):
        """Démarre le suivi de l'objet à partir de la source vidéo."""
        try:
            while not self.stop_event.is_set():
                response = self.websocket_client.response
                found, servo_horizontal_angle, servo_vertical_angle, speed, is_close = response
                self.arduino_comm.send_data(servo_horizontal_angle, servo_vertical_angle, speed, is_close)
                if not found:
                    self.arduino_comm.send_data(servo_horizontal_angle, servo_vertical_angle, 0, rotate=True)

                distance = self.arduino_comm.receive_distance()
                if distance and distance < 10:  # Ex. seuil pour l'arrêt
                    self.stop_event.set()
                    break

        except Exception as e:
            print(f"Erreur lors du suivi : {e}")
