import asyncio
import websockets


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()

    async def handle_client(self, websocket):
        self.clients.add(websocket)
        print(f'New client connected: {websocket.remote_address}')

        try:
            async for message in websocket:
                print(f'Received message from {websocket.remote_address}: {message}')
                await self.broadcast(message)
        except websockets.exceptions.ConnectionClosedError:
            pass
        finally:
            self.clients.remove(websocket)
            print(f'Client disconnected: {websocket.remote_address}')

    async def broadcast(self, message):
        for client in self.clients:
            await client.send(message)

    async def start(self):
        self.server = await websockets.serve(self.handle_client, self.host, self.port)
        print(f'Server started at {self.host}:{self.port}')

        await self.server.wait_closed()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

def run_server():
    server = WebSocketServer('localhost', 8800)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(server.start())
    finally:
        loop.run_until_complete(server.stop())

# Chạy server
run_server()