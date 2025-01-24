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

    def init_tracker(self):
        try:
            self.tracker = ObjectTracker(source='stream', stream_url='http://172.20.10.8', target_name='person')
        except Exception as e:
            self.error = f"erreur lors de l'initialisation du serveur: {e}"
            print(self.error)

    def process_message(self, data):
        """
        Process the message received from the client.

        :param data: The JSON message sent by the client.
        :return: A response to send back to the client.
        """
        try:
            # Handle the stop signal
            self.stop = data.get("stop", False)
            if stop:
                self.running = False
                return {"status": "server_stopping"}

            # Handle different message types
            message_type = data.get("type")
            if message_type == "target_name":
                target_name = data.get("data")
                if target_name:
                    return {"status": "success", "type": "target_name", "target_name": target_name}
                else:
                    return {"error": "Missing target name"}

            elif message_type == "image":
                encoded_image = data.get("data")
                filename = data.get("filename", "received_image.jpg")
                if encoded_image:
                    # Decode and save the image
                    image_bytes = base64.b64decode(encoded_image)
                    # Define the folder to save the image
                    save_path = r"C:\Users\ELEONOR BJOUNKENG\Pictures\NUT"
                    os.makedirs(save_path, exist_ok=True)  # Ensure the folder exists
                    full_file_path = os.path.join(save_path, filename)
                    with open(full_file_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    print(f"Image saved to {full_file_path}")
                    return {"status": "success", "type": "image", "filename": filename, "path": full_file_path}
                else:
                    return {"error": "Missing image data"}

            return {"error": "Unknown message type"}
        except Exception as e:
            return {"error": f"Internal server error: {str(e)}"}

    async def handle_client(self, websocket, path=None):
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(f"Message reçu : {data}")

                    # Process the message and send a response
                    response = self.process_message(data)
                    await websocket.send(json.dumps(response))

                    # Stop the server if the running flag is set to False
                    if not self.running:
                        print("Arrêt du serveur sur demande du client.")
                        break

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

    async def start(self):
        server = await websockets.serve(
            self.handle_client, 
            self.host, 
            self.port
        )
        print(f"Serveur WebSocket démarré sur ws://{self.host}:{self.port}")
        await server.wait_closed()

    async def stop(self):
        """
        Fonction pour fermer le serveur proprement
        """
        print("Arrêt du serveur WebSocket.")
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
