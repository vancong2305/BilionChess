import asyncio
import websockets


class WebSocketClient:
    client = None
    def __init__(self, server_uri):
        self.server_uri = server_uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.server_uri)

    async def send_message(self, message):
        await self.websocket.send(message)

    async def receive_message(self):
        return await self.websocket.recv()

    async def close(self):
        await self.websocket.close()
