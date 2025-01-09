import asyncio
import websockets

# Function to handle the chat client
class Client:
    def __init__(self, addressIP="localhost", port="12345"):
        self.addressIP = addressIP
        self.port = port
        self.flag = True
        self.response = None
        pass

    async def receive(self):
        try:
            async with websockets.connect(f"ws://{self.addressIP}:{self.port}") as websocket:
                while self.flag:
                    # Receive a message from the server
                    self.response = await websocket.recv()
        except Exception as e:
            raise e
        
    async def send(self, message):
        try:
            async with websockets.connect(f"ws://{self.addressIP}:{self.port}") as websocket:
                await websocket.send(message)
        except Exception as e:
            raise e
        
    def stop(self):
        self.flag = False
        self.send(self.flag)
