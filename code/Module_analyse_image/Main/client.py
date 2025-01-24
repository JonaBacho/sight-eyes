import asyncio
import websockets
import json

class Client:
    def __init__(self, addressIP="localhost", port="12346"):
        self.addressIP = addressIP
        self.port = port
        self.websocket = None

     # Fonction pour établir une connexion WebSocket avec le serveur.
    async def connect(self):
        try:
            self.websocket = await websockets.connect(f"ws://{self.addressIP}:{self.port}")
            print(f"Connexion établie avec ws://{self.addressIP}:{self.port}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            raise

    # Fonction pour envoyer un message au serveur.
    async def send(self, message):
       
        try:
            if self.websocket is None:
                await self.connect()
            await self.websocket.send(message)
            print(f"Message envoyé : {message}")
        except Exception as e:
            print(f"Erreur lors de l'envoi : {e}")
            raise

    # Fonction pour recevoir un message du serveur.
    async def receive(self):
        try:
            if self.websocket:
                message = await self.websocket.recv()
                print(f"Message reçu : {message}")
                return message
        except Exception as e:
            print(f"Erreur lors de la réception : {e}")
            raise

    #Fermeture de la connexion WebSocket.
    async def close(self):
    
        if self.websocket:
            await self.websocket.close()
            print("Connexion fermée")



async def test_client():
    """
    Fonction de test pour le client.
    """
    client = Client()
    try:
        await client.connect()
        await client.send(json.dumps({"target": "example"}))  # Envoi d'un exemple de message
        response = await client.receive()  # Réception de la réponse
        print(f"Réponse du serveur : {response}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_client())
