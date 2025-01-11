import time
from arduino import ArduinoCommunication
from threading import Event
from client import Client

class Core:
    def __init__(self, image=None, server_address="localhost", port="12345"):
        """
        Initialise le tracker d'objets.

        :param image: Image pour identifier l'objet cible.
        :param server_address: adresse IP du serveur websocket.
        :param port: port pour le client websocket.
        """
        self.image = image

        # Initialisation des variables
        self.activate_bip = False
        self.found = False
        self.servo_horizontal_angle = 90
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

    def resume_tracking(self):
        self.stop_event.clear()
        
    def bip(self):
        self.activate_bip = True
        self.arduino_comm.send_data(self.current_speed, self.servo_horizontal_angle, not self.found, not self.stop_event.is_set, self.activate_bip)
        time.sleep(5)
        self.activate_bip = False

    def start_tracking(self):
        """Démarre le suivi de l'objet à partir de la source vidéo."""
        try:
            while not self.stop_event.is_set():
                response = self.websocket_client.response
                self.found, self.servo_horizontal_angle, self.current_speed = response
                self.arduino_comm.send_data(self.current_speed, self.servo_horizontal_angle, not self.found, not self.stop_event.is_set, self.activate_bip)
                if not self.found:
                    self.current_speed, self.activate_bip = 0, False
                    self.arduino_comm.send_data(self.current_speed, self.servo_horizontal_angle, not self.found, not self.stop_event.is_set, self.activate_bip)

                distance = self.arduino_comm.receive_distance()
                if self.found and distance and distance < 10:  # Ex. seuil pour l'arrêt
                    self.stop_event.set()
                    self.bip()
                    break

        except Exception as e:
            print(f"Erreur lors du suivi : {e}")
