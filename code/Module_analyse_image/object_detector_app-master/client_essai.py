import json

from websockets.sync.client import connect
import time

class WebSocketClient:
    def __init__(self, server_ip="192.168.1.179", server_port=12346):
        """
        Constructeur du client WebSocket.
        :param server_ip: Adresse IP du serveur (ex: "localhost").
        :param server_port: Port du serveur (ex: 8765).
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_url = f"ws://{self.server_ip}:{self.server_port}"
        self.websocket = None

    def connect(self):
        """
        Établit une connexion WebSocket avec le serveur.
        """
        try:
            print(f"Connexion au serveur WebSocket à {self.server_url}...")
            self.websocket = connect(self.server_url)
            print("Connexion établie avec succès.")
        except Exception as e:
            print(f"Erreur lors de la connexion au serveur : {e}")
            raise

    def send_message(self, message):
        """
        Envoie un message au serveur.
        :param message: Le message à envoyer
        """
        if self.websocket is None:
            print("Erreur : Aucune connexion WebSocket n'est établie.")
            return

        try:
            print(f"Envoi du message : {message}")
            self.websocket.send(message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du message : {e}")
            raise

    def receive_message(self):
        """
        Reçoit un message du serveur.
        :return: Le message reçu.
        """
        if self.websocket is None:
            print("Erreur : Aucune connexion WebSocket n'est établie.")
            return None

        try:
            print("ici_receive")
            message = self.websocket.recv()
            print(f"Message reçu du serveur : {message}")
            return message
        except Exception as e:
            print(f"Erreur lors de la réception du message : {e}")
            raise

    def close(self):
        """
        Ferme la connexion WebSocket proprement.
        """
        if self.websocket is not None:
            print("Fermeture de la connexion WebSocket...")
            self.websocket.close()
            self.websocket = None
            print("Connexion fermée.")
        else:
            print("Aucune connexion WebSocket à fermer.")

    def run(self):
        """
        Méthode principale pour interagir avec le serveur.
        """
        try:
            self.connect()

            message = {
                "message_type": "target_name",
                "data": "person",
                "stop": False
            }

            # Exemple d'interaction avec le serveur
            self.send_message(json.dumps(message))  # Démarrer la boucle infinie
            time.sleep(5)  # Attendre 5 secondes

            # Recevoir des messages du serveur pendant un certain temps
            start_time = time.time()
            while time.time() - start_time < 10:  # Recevoir pendant 10 secondes
                print("ici")
                self.receive_message()
                time.sleep(0.5)  # Attendre 500 ms entre chaque réception

            message['stop'] = True
            self.send_message(json.dumps(message))  # Arrêter la boucle infinie
        except Exception as e:
            print(f"Erreur lors de l'exécution du client : {e}")
        finally:
            self.close()

# Programme principal
if __name__ == "__main__":
    client = WebSocketClient("192.168.8.105", 12346)
    client.run()