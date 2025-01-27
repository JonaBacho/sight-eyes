import asyncio
import websockets
import json
from tracker import ObjectTracker
import base64
import os
import threading
import time
from websockets.sync.server import serve
from websockets.exceptions import ConnectionClosedError

class Server:
    def __init__(self, host="192.168.1.179", port=12346):
        self.host = host
        self.port = port
        self.error = None
        #self.connected_clients = set()
        self.tracker = None
        self.stop = True
        self.send_running = False
        self.image_path = None
        self.target_name = None
        self.loop_thread = None
        self.send_thread = None

    def init_tracker(self, target_name=None, image_path=None):
        try:
            if target_name:
                self.tracker = ObjectTracker(source='webcam', stream_url='http://172.20.10.8', target_name=target_name)
                return
            elif image_path:
                self.tracker = ObjectTracker(source='webcam', stream_url='http://172.20.10.8', image_path=image_path)
        except Exception as e:
            self.error = f"erreur lors de l'initialisation du serveur: {e}"
            print(self.error)

    def process_message(self, data):
        try:
            self.stop = data.get("stop")
            message_type = data.get("message_type")
            if message_type == "target_name":
                self.target_name = data.get("data")

            elif message_type == "image":
                encoded_image = data.get("data")
                filename = data.get("filename")
                if encoded_image:
                    image_bytes = base64.b64decode(encoded_image)
                    save_path = os.getcwd() + os.sep + "image"
                    os.makedirs(save_path, exist_ok=True)
                    full_file_path = os.path.join(save_path, filename)
                    with open(full_file_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    print(f"Image saved to {full_file_path}")
                    self.image_path = full_file_path
                else:
                    self.error = "Missing image data"

            else:
                self.error = "Unknown message type"
        except Exception as e:
            self.error = f"Internal server error: {str(e)}"

    def send_attributes(self, websocket):
        """
        Méthode exécutée dans un thread séparé pour envoyer les attributs au client.
        """
        while self.send_running:
            try:
                # Envoyer l'attribut de l'objet A au client toutes les 500 ms
                print(self.tracker)
                response_data = {
                    'speed': float(self.tracker.current_speed),
                    'horizontal_angle': float(self.tracker.servo_horizontal_angle),
                    'object_found': self.tracker.object_found
                }
                response = {
                    'data': response_data,
                    'error': self.error
                }
                print("message pret")
                websocket.send(json.dumps(response))
                print("envoyé")
                time.sleep(0.5)

            except json.JSONDecodeError:
                error_response = {"error": "Invalid JSON format"}
                websocket.send(json.dumps(error_response))
            except ConnectionClosedError:
                print("Client déconnecté pendant l'envoi des attributs")
                break
            except Exception as e:
                print(f"Erreur lors de l'envoi des attributs : {e}")
                break

    def handle_client(self, websocket, path=None):
        while True:
            # Attendre un message du client
            message = websocket.recv()
            data = json.loads(message)
            print(f"Message reçu du client : {data}")

            self.process_message(data)
            print("process message finished !")
            print(self.stop)
            if not self.stop and self.tracker is None:
                self.init_tracker(self.target_name, self.image_path)
                self.loop_thread = threading.Thread(target=self.tracker.start_tracking)
                self.loop_thread.start()
                time.sleep(5) # on attends deux secondes le temps que le model se lance effectivement

                print("Boucle infinie démarrée")
                print(self.tracker)
                # Démarrer l'envoi des attributs dans un thread séparé
                self.send_running = True
                self.send_thread = threading.Thread(target=self.send_attributes, args=(websocket,))
                self.send_thread.start()

            elif self.stop and self.tracker is not None:
                # Arrêter la boucle infinie si elle est active
                print("fin")
                self.tracker.stop_tracking()
                self.send_running = False  # Arrêter le thread d'envoi
                self.send_thread.join()  # Attendre que le thread d'envoi se termine
                self.loop_thread.join()  # Attendre que la boucle infinie se termine
                self.tracker = None
                self.loop_thread = None
                print("Boucle infinie arrêtée")


    async def broadcast_updates(self):
        """
        Diffuse un message périodique à tous les clients connectés.
        """
        while not self.stop:
            if self.connected_clients:
                message = {
                    'info': 'Mise à jour périodique',
                    'data': {
                        'speed': self.tracker.current_speed if self.tracker else None,
                        'horizontal_angle': self.tracker.servo_horizontal_angle if self.tracker else None,
                        'object_found': self.tracker.object_found if self.tracker else False
                    },
                    'error': self.error
                }
                await asyncio.gather(*[client.send(json.dumps(message)) for client in self.connected_clients])
            await asyncio.sleep(0.5)  # Pause de 500 ms

    def start(self):
        with serve(self.handle_client, self.host, self.port) as server:
            print(f"Serveur WebSocket démarré sur ws://{self.host}:{self.port}")
            server.serve_forever()

    async def stop(self):
        """
        Ferme le serveur proprement.
        """
        print("Arrêt du serveur WebSocket.")
        self.stop = True
        await asyncio.gather(*[client.close() for client in self.connected_clients])


if __name__ == "__main__":
    server = Server(host="192.168.8.105")
    server.start()
