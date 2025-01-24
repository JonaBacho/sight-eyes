
import asyncio
import websockets
import json
#from tracker import Tracker  # Assurez-vous que tracker.py est dans le même répertoire
class Server:
    def _init_(self, host="172.20.10.5", port=8765):
        self.host = host
        self.port = port
        #self.tracker = Tracker()

    async def handle_client(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            target = data.get('target')
            if target:
                #speed, angle, success = self.tracker.analyze(target)
                speed, angle, success = 0.9, 12, True
                response = {
                    'speed': speed,
                    'angle': angle,
                    'success': success
                }
                await websocket.send(json.dumps(response))

    async def start(self):
        server = await websockets.serve(self.handle_client, self.host, self.port)
        await server.wait_closed()

if __name__ == "_main_":
    server = Server()
    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()