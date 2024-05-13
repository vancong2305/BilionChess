import asyncio

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.ready.IdentifyScreen import IdentifyScreen
from src.client.handle.RoomRequest import RoomRequest

import asyncio

async def main():
    client = WebSocketClient('ws://localhost:8800')
    await client.connect()
    await IdentifyScreen().run()

# Chạy mã bất đồng bộ
asyncio.run(main())