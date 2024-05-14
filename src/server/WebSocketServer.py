import asyncio
import websockets
import json

from src.server.sevice.MatchService import MatchService
from src.server.sevice.RoomService import RoomService
from src.server.sevice.UserService import UserService


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()

    async def remove(self, id):
        await UserService().delete(id)
        await RoomService().hard_delete(id)
        for match in MatchService.matchs:
            if match["match_id"] == id:
                MatchService.matchs.remove(match)  # Xóa phần tử

    async def handle_client(self, websocket):
        self.clients.add(websocket)
        print(f'New client connected: {websocket.remote_address}')

        try:
            # Gửi tham số 'address[1]' đến khách hàng
            await websocket.send(str(websocket.remote_address[1]))

            async for message in websocket:
                print(f'Received message from {websocket.remote_address}: {message}')
                # Xử lý yêu cầu JSON từ khách hàng
                try:
                    request = json.loads(message)
                    # Check điều kiện
                    if 'object' in request and 'action' in request:
                        if request['object'] == 'room':
                            await RoomService().process_request(request, websocket.remote_address[1], websocket, self.clients)

                    if 'object' in request and 'action' in request:
                        if request['object'] == 'user':
                            response = UserService().process_request(request, websocket.remote_address[1], self.clients)
                            await websocket.send(json.dumps(response))

                    if 'object' in request and 'action' in request:
                        if request['object'] == 'match':
                            await MatchService().process_request(request, websocket.remote_address[1], websocket, self.clients)

                except json.JSONDecodeError:
                    response = {'status': 'error', 'message': 'Invalid request'}
                    await websocket.send(json.dumps(response))
                    print('Invalid JSON format')
        except websockets.exceptions.ConnectionClosedError:

            await self.remove(websocket.remote_address[1])
            self.clients.remove(websocket)
            pass
        finally:
            await self.remove(websocket.remote_address[1])
            self.clients.remove(websocket)
            print(f'Client disconnected: {websocket.remote_address}')

    def process_request(self, request):
        # Xử lý yêu cầu từ khách hàng và trả về phản hồi tương ứng
        # Ví dụ đơn giản: Trả về yêu cầu ban đầu
        return request

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