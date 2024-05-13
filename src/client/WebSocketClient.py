import asyncio
import websockets
from queue import Queue

class WebSocketClient:
    client = None
    id = None
    message_queue = None
    def __init__(self, server_uri):
        self.server_uri = server_uri
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.server_uri)
        response = await self.websocket.recv()
        WebSocketClient.id = response
        WebSocketClient.client = self.websocket
        WebSocketClient.message_queue = Queue()

    async def send_message(self, message):
        await self.websocket.send(message)

    async def receive_message(self):
        return await self.websocket.recv()
    def get_next_message(self):
        return WebSocketClient.message_queue.get()

    async def close(self):
        await self.websocket.close()