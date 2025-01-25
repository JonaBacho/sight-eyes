import asyncio
import websockets
import json
from tracker import ObjectTracker
import base64
import os
from threading import Thread

class Server:
    def __init__(self, host="localhost", port=12346):
        self.host = host
        self.port = port
        self.error = None
        self.connected_clients = set()
        self.tracker = None
        self.stop = False
        self.running = True

    def init_tracker(self, target_name=None, image_path=None):
        try:
            if target_name:
                self.tracker = ObjectTracker(source='webcam', stream_url='http://172.20.10.8', target_name=target_name)
                return
            elif image_path:
                self.tracker = ObjectTracker(source='stream', stream_url='http://172.20.10.8', image_path=image_path)
        except Exception as e:
            self.error = f"erreur lors de l'initialisation du serveur: {e}"
            print(self.error)

    def process_message(self, data):
        try:
            # Handle the stop signal
            self.stop = data.get("stop", False)
            if self.stop:
                self.running = False
                return {"status": "server_stopping"}

            # Handle different message types
            message_type = data.get("type")
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

            self.stop = data.get("stop", False)
            if not self.stop:
                if self.first_communication == -1:
                    self.init_tracker(self.target_name, self.image_path)
                    self.first_communication = 1
                    Thread(target=self.tracker.start_tracking).start()

            self.error = "Unknown message type"
        except Exception as e:
            self.error = f"Internal server error: {str(e)}"

    async def handle_client(self, websocket, path=None):
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(f"Message reçu : {data}")

                    self.process_message(data)
                    response_data = {
                        'speed': self.tracker.current_speed,
                        'horizontal_angle': self.tracker.servo_horizontal_angle,
                        'object_found': self.tracker.object_found
                    }
                    response = {
                        'data': response_data,
                        'error': self.error
                    }
                    await websocket.send(json.dumps(response))

                except json.JSONDecodeError:
                    error_response = {"error": "Invalid JSON format"}
                    await websocket.send(json.dumps(error_response))
                except Exception as e:
                    print(f"Erreur de traitement du message : {e}")
                    await websocket.send(json.dumps({"error": "Internal server error"}))

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connexion fermée : {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
        finally:
            self.connected_clients.remove(websocket)

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

    async def start(self):
        broadcast_task = asyncio.create_task(self.broadcast_updates())
        server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f"Serveur WebSocket démarré sur ws://{self.host}:{self.port}")
        await server.wait_closed()
        broadcast_task.cancel()  # Annule la tâche de diffusion périodique

    async def stop(self):
        """
        Ferme le serveur proprement.
        """
        print("Arrêt du serveur WebSocket.")
        self.stop = True
        await asyncio.gather(*[client.close() for client in self.connected_clients])


async def main():
    server = Server()
    try:
        await server.start()
    except KeyboardInterrupt:
        print("Serveur interrompu.")
        await server.stop()

if __name__ == "__main__":
    asyncio.run(main())
