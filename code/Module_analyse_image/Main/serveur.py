import asyncio
import websockets
import json

class Server:
    def __init__(self, host="localhost", port=12346):
        self.host = host
        self.port = port
        self.connected_clients = set()

    def process_message(self, data):
        """
        Méthode séparée pour traiter les messages 
        À personnaliser avec vos calculs spécifiques
        """
        target = data.get('target')
        if target:
            # Exemple de traitement
            return {
                'speed': 0.9,  # Exemple de valeur
                'angle': 12,   # Exemple de valeur
                'success': True
            }
        return {'error': 'No target provided'}

    async def handle_client(self, websocket, path=None):
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)  # Vérifiez si le message reçu est un JSON valide
                    response = self.process_message(data)
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
