import asyncio
import json
from threading import Event
from client import Client  # Assurez-vous que la classe Client est correctement importée

class Core:
    def __init__(self, image=None, target_name=None, server_address="localhost", port="12345"):
        """
        Initialise le tracker d'objets.

        :param image: Image pour identifier l'objet cible.
        :param server_address: adresse IP du serveur websocket.
        :param port: port pour le client websocket.
        """
        self.image = image
        self.target_name = target_name
        self.server_address = server_address
        self.port = port

        # Initialisation des variables
        self.activate_bip = False
        self.found = False
        self.servo_horizontal_angle = 90
        self.current_speed = 0  # Vitesse initiale
        self.stop_event = Event()
        self.websocket_client = Client(server_address, port)
        self.response = None  # Pour stocker la réponse du serveur

    async def initialize_target(self):
        """
        Identifie l'objet cible en envoyant une image ou un nom de cible au serveur.
        """
        try:
            await self.websocket_client.connect()
            if self.image:
                # Envoyer une image au serveur
                await self.websocket_client.send(stop=False, message_type="image", data=self.image)
            elif self.target_name:
                # Envoyer un nom de cible au serveur
                await self.websocket_client.send(stop=False, message_type="target_name", data=self.target_name)
            else:
                raise ValueError("Aucune image ou nom de cible fourni.")

            # Recevoir la réponse initiale du serveur
            self.response = await self.websocket_client.receive()
            print(f"Réponse initiale du serveur : {self.response}")

        except Exception as e:
            print(f"Erreur lors de l'initialisation de la cible : {e}")
            raise e

    async def start_tracking(self):
        """
        Démarre le suivi de l'objet.
        """
        await self.initialize_target()
        try:
            while not self.stop_event.is_set():
                # Recevoir les données du serveur
                self.response = await self.websocket_client.receive()
                print(f"Réponse du serveur : {self.response}")

                # Traiter la réponse
                if self.response:
                    data = json.loads(self.response)
                    self.found = data.get("found", False)
                    self.servo_horizontal_angle = data.get("servo_horizontal_angle", 90)
                    self.current_speed = data.get("current_speed", 0)

                # Si l'objet n'est pas trouvé, arrêter le mouvement
                if not self.found:
                    self.current_speed = 0
                    self.activate_bip = False

                # Simuler la communication avec Arduino (remplacez par votre logique réelle)
                print(f"Envoi à Arduino : Vitesse={self.current_speed}, Angle={self.servo_horizontal_angle}, "
                     f"Trouvé={self.found}, Bip={self.activate_bip}")

                # Simuler la réception d'une distance d'objets
                distance = 15  # Exemple de valeur de distance
                if self.found and distance < 10:  # Seuil pour l'arrêt
                    self.stop_event.set()
                    await self.bip()

        except Exception as e:
            print(f"Erreur pendant le suivi : {e}")
            raise e

    async def bip(self):
        """
        Active le bip pendant quelques secondes.
        """
        self.activate_bip = True
        
        print("Bip activé !")
        await asyncio.sleep(5)
        self.activate_bip = False
        print("Bip désactivé.")

    async def stop_tracking(self):
        """
        Arrête le suivi de l'objet.
        """
        self.stop_event.set()
        await self.websocket_client.send(stop=True, message_type="command", data="stop")
        await self.websocket_client.close()

