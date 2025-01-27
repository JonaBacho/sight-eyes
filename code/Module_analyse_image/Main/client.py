import asyncio
from websockets.sync.client import connect
import json
import base64


class Client:
    def __init__(self, addressIP="localhost", port="12346"):
        self.addressIP = addressIP
        self.port = port
        self.websocket = None

    def connect(self):
        try:
            self.websocket = connect(f"ws://{self.addressIP}:{self.port}")
            print(f"Connexion établie avec ws://{self.addressIP}:{self.port}")
        except Exception as e:
            raise RuntimeError(f"Erreur de connexion : {e}")

    def send(self, stop, message_type, data):
        """
        Send a message to the server.

        :param stop: Boolean to indicate whether the server should continue running.
        :param message_type: "image" or "target_name".
        :param data: The target name (string) or image file path.
        """
        try:
            if self.websocket is None:
                self.connect()

            # Prepare the message
            if message_type == "image":
                # Read and encode the image as base64
                encoded_image = base64.b64encode(data).decode("utf-8")
                #payload = {"stop": stop, "type": "image", "data": encoded_image, "filename": filename or "image.jpg"}
                payload = {"stop": False, "type": "image", "data": encoded_image}
                
       
            elif message_type == "target_name":
                payload = {"stop": False, "type": "target_name", "data": data}
            else:
                raise ValueError("Invalid message type. Must be 'image' or 'target_name'.")

            # Send the JSON message
            self.websocket.send(json.dumps(payload))
            print(f"Message envoyé : {payload}")
        except Exception as e:
            raise RuntimeError(f"Erreur de l'envoi : {e}")

    def receive(self):
        try:
            if self.websocket:
                message = self.websocket.recv()
                print(f"Message reçu : {message}")
                return message
        except Exception as e:
            print(f"Erreur lors de la réception : {e}")
            raise

    def close(self):
        if self.websocket:
            self.websocket.close()
            self.websocket = None
            print("Connexion fermée")


def test_client():
    """
    Test the client by sending a target name and an image.
    """
    client = Client()
    try:
        client.connect()

        # Send a target name
        client.send(stop=False, message_type="target_name", data="person")

        # Send an image
        #await client.send(stop=False, message_type="image", data="C:/Users/DELL/Pictures/vroom.jpeg")

        # Stop the server
        #await client.send(stop=True, message_type="target_name", data="shutdown")

        # Receive a response from the server
        response = client.receive()
        print(f"Réponse du serveur : {response}")

    except Exception as e:
        print(f"Erreur : {e}")
     #finally:
         #await client.close()


if __name__ == "__main__":
    test_client()
