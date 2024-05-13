import json

from src.client.WebSocketClient import WebSocketClient


class RoomRequest:
    def __init__(self):
        self.client = WebSocketClient.client

    async def join_room(self, owner):
        request = {
            "object": "room",
            "action": "join",
            "room_id": owner
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        response_data = json.loads(response)
        # Xử lý phản hồi từ server theo nhu cầu của bạn

    async def get_by_owner(self, owner):
        request = {
            "object": "room",
            "action": "get",
            "room_id": owner
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        response_data = json.loads(response)
        # Xử lý phản hồi từ server theo nhu cầu của bạn

    async def get(self):
        request = {
            "object": "room",
            "action": "get_all"
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        return json.loads(response)
        # Xử lý phản hồi từ server theo nhu cầu của bạn
    async def create(self):
        request = {
            "object": "room",
            "action": "create"
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        response_data = json.loads(response)
        print(response_data)
        # Xử lý phản hồi từ server theo nhu cầu của bạn