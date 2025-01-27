import asyncio
import websockets
import json
import base64


class Client:
    def __init__(self, addressIP="192.168.8.105", port="12346"):
        self.addressIP = addressIP
        self.port = port
        self.websocket = None

    async def connect(self):
        try:
            self.websocket = await websockets.connect(f"ws://{self.addressIP}:{self.port}")
            print(f"Connexion établie avec ws://{self.addressIP}:{self.port}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            raise

    async def send(self, stop, message_type, data):
        """
        Send a message to the server.

        :param stop: Boolean to indicate whether the server should continue running.
        :param message_type: "image" or "target_name".
        :param data: The target name (string) or image file path.
        """
        try:
            if self.websocket is None:
                await self.connect()

            # Prepare the message
            if message_type == "image":
                # Read and encode the image as base64
                encoded_image = base64.b64encode(data).decode("utf-8")
                #payload = {"stop": stop, "type": "image", "data": encoded_image, "filename": filename or "image.jpg"}
                payload = {"stop": False, "message_type": "image", "data": encoded_image}
                
       
            elif message_type == "target_name":
                payload = {"stop": False, "message_type": "target_name", "data": data}
            else:
                raise ValueError("Invalid message type. Must be 'image' or 'target_name'.")

            # Send the JSON message
            await self.websocket.send(json.dumps(payload))
            print(f"Message envoyé : {payload}")
        except Exception as e:
            print(f"Erreur lors de l'envoi : {e}")
            raise

    async def receive(self):
        try:
            if self.websocket:
                message = await self.websocket.recv()
                print(f"Message reçu : {message}")
                return message
        except Exception as e:
            print(f"Erreur lors de la réception : {e}")
            raise

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("Connexion fermée")


async def test_client():
    """
    Test the client by sending a target name and an image.
    """
    client = Client()
    try:
        await client.connect()

        # Send a target name
        await client.send(stop=False, message_type="target_name", data="person")

        # Send an image
        #await client.send(stop=False, message_type="image", data="C:/Users/DELL/Pictures/vroom.jpeg")

        # Stop the server
        #await client.send(stop=True, message_type="target_name", data="shutdown")

        # Receive a response from the server
        response = await client.receive()
        print(f"Réponse du serveur : {response}")

    except Exception as e:
        print(f"Erreur : {e}")
     #finally:
         #await client.close()


if __name__ == "__main__":
    asyncio.run(test_client())
