import asyncio

from src.client.WebSocketClient import WebSocketClient
from src.client.gui.parameter.Connect import Connect
from src.client.gui.ready.IdentifyScreen import IdentifyScreen
from src.client.handle.RoomRequest import RoomRequest

import asyncio

async def xys():
    Connect.ID = WebSocketClient.id  # Gán giá trị cho Connect.ID

async def main():
    client = WebSocketClient('ws://localhost:8800')
    await client.connect()
    await asyncio.sleep(1)  # Tạm dừng thực thi trong 1 giây
    task = asyncio.create_task(xys())  # Tạo task từ hàm xys()
    await task  # Đợi task hoàn thành
    print(Connect.ID)
    await IdentifyScreen().run()

# Chạy mã bất đồng bộ
asyncio.run(main())