import json

from src.client.WebSocketClient import WebSocketClient


class NameRequest:
    def __init__(self):
        self.client = WebSocketClient.client

    async def create_user(self, user_name):
        request = {
            "object": "user",
            "action": "create",
            "user_name": user_name
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        response_data = json.loads(response)