import asyncio

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.ready.IdentifyScreen import IdentifyScreen

async def main():
    client = WebSocketClient('ws://localhost:8800')
    WebSocketClient.client = await client.connect()
    IdentifyScreen().run()

# Chạy mã bất đồng bộ
asyncio.run(main())