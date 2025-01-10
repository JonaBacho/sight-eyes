import os
import numpy as np
from arduino import ArduinoCommunication
from threading import Event
from client import Client

class Core:
    def __init__(self, image=None, server_address="localhost", port="12345"):
        """
        Initialise le tracker d'objets.

        :param image_path: Chemin vers une image pour identifier l'objet cible.
        :param target_name: Nom de l'objet cible parmi les 90 reconnus.
        :param server_address: adresse IP du serveur websocket.
        :param port: port pour le client websocket.
        """
        self.image = image

        # Initialisation des variables
        self.activate_bip = False
        self.is_close = False
        self.servo_horizontal_angle = 90
        self.servo_vertical_angle = 90
        self.current_speed = 0  # Vitesse initiale
        self.arduino_comm = ArduinoCommunication(port='LPT1', baudrate=9600)
        self.stop_event = Event()
        self.websocket_client = Client(server_address,port)

        # Identifie l'objet cible
        try:
            self.websocket_client.receive()
            if self.image:
                self.target_id = self.websocket_client.send(self.image)
            
        except Exception as e:
            raise e

    def stop_tracking(self):
        self.stop_event.set()
        self.websocket_client.stop()
        self.bip()

    def resume_tracking(self):
        self.stop_event.clear()
        
    def bip(self):
        self.activate_bip = True
        self.arduino_comm.send_data(self.servo_horizontal_angle, self.servo_vertical_angle, self.current_speed, self.is_close, self.activate_bip)
        self.activate_bip = False

    def start_tracking(self):
        """Démarre le suivi de l'objet à partir de la source vidéo."""
        try:
            while not self.stop_event.is_set():
                response = self.websocket_client.response
                found, self.servo_horizontal_angle, self.servo_vertical_angle, self.current_speed, self.is_close = response
                self.arduino_comm.send_data(self.servo_horizontal_angle, self.servo_vertical_angle, self.current_speed, self.is_close, self.activate_bip)
                if not found:
                    self.current_speed, self.is_close, self.activate_bip = 0, True, False
                    self.arduino_comm.send_data(self.servo_horizontal_angle, self.servo_vertical_angle, self.current_speed, self.is_close, self.activate_bip)

                distance = self.arduino_comm.receive_distance()
                if found and distance and distance < 10:  # Ex. seuil pour l'arrêt
                    self.stop_event.set()
                    break

        except Exception as e:
            print(f"Erreur lors du suivi : {e}")
