import json

from src.client.WebSocketClient import WebSocketClient


class MatchRequest:
    def __init__(self):
        self.client = WebSocketClient.client

    async def update_match(self, item_id, match_id):
        request = {
            "object": "match",
            "action": "update",
            "item_id": item_id,
            "match_id": match_id
        }
        await WebSocketClient.client.send(json.dumps(request))
        response = await WebSocketClient.client.recv()
        response_data = json.loads(response)
        # Xử lý phản hồi từ server theo nhu cầu của bạn

    async def create_match(self):
        request = {
            "object": "match",
            "action": "create"
        }
        await WebSocketClient.client.send(json.dumps(request))