import asyncio
import json

from src.server.dto.Match import Match
from src.server.sevice.RoomService import RoomService
from src.server.sevice.UserService import UserService
import random


class MatchService:
    matchs = []
    lock = asyncio.Lock()
    def __init__(self):
        self.client = None
        self.clients = None
        self.user_id = None
        self.timer_task = None  # Thêm thuộc tính timer_task để lưu trữ task của bộ đếm ngược

    async def process_request(self, request, user_id, client, clients):
        self.client = client
        self.clients = clients
        self.user_id = user_id

        action = request['action']
        if action == 'get_all':
            await self.get_all_matchs()
        elif action == 'update':
            item_id = request.get('item_id')
            match_id = request.get('match_id')
            await self.update_match(item_id, match_id, user_id)
        elif action == 'create':
            await self.create_match(self.user_id)
        else:
            # Nếu yêu cầu không phù hợp với các điều kiện trên, trả về phản hồi lỗi
            response = {'status': 'error', 'message': 'Invalid request'}
            await self.client.send(json.dumps(response))

    async def get_all_matchs(self):
        # Xử lý yêu cầu lấy tất cả các phòng
        # Ví dụ: Trả về danh sách các phòng
        response = {'status': 'success', 'message': 'All matchs retrieved', 'matchs': MatchService.matchs}
        await self.client.send(json.dumps(response))

    async def create_match(self, user_id):
        # Lấy tất cả user_id của thành viên trong phòng
        room = RoomService.get_rooms_by_room_id(user_id)
        print(room['members'])
        # Tạo match mới
        Match()
        match = Match.match
        print(user_id.__str__() + "user_id")
        match['match_id'] = user_id
        match['users'][0]['user_id'] = room['members'][0]['user_id']
        match['users'][1]['user_id'] = room['members'][1]['user_id']
        print(match['users'][0]['user_id'].__str__() + "is 1")
        print(match['users'][1]['user_id'].__str__() + "is 2")
        MatchService.matchs.append(match)
        print(MatchService.matchs)
        # Gửi request đến những user chỉ định
        await self.send_response_to_members(room['members'], match)
        await asyncio.sleep(2)
        turn_id_1 = int(room['members'][0]['user_id'])
        turn_id_2 = int(room['members'][1]['user_id'])
        # Tạo task riêng để đếm ngược 30 giây
        self.timer_task = asyncio.create_task(self.start_match(room['members'], user_id, turn_id_1, turn_id_2))
    async def start_match(self, member, user_id, turn_id_1, turn_id_2):
        remaining_time = 30
        uid = user_id
        t1 = turn_id_1
        t2 = turn_id_2
        turn = t1
        boolean_check = True

        while boolean_check:
            await asyncio.sleep(1)
            response = {
                "remaining_time": remaining_time
            }
            await self.send_response_to_members(member, response)
            remaining_time -= 1
            for match in MatchService.matchs:
                if match.get('match_id') == uid:
                    # Quay xúc sắc và gửi lại response cho user nếu lượt này chưa roll, cập nhật lại vị trí của user
                    match['turn_id'] = turn
                    if (match["roll"] == 0):
                        random_number = self.random_1_to_6()
                        match['dice'] = random_number
                        for user in match["users"]:
                            if user.get('user_id') == match['turn_id']:
                                user['gold'] = user.get('gold') + random_number * 100
                                positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                             21, 22, 23, 24]
                                current_position = user.get('index')
                                selected_positions = []
                                for i in range(current_position + 1, current_position + random_number + 1):
                                    position_index = (i - 1) % len(positions)
                                    selected_positions.append(positions[position_index])
                                for selected_position in selected_positions:
                                    p = match['positions'][selected_position - 1]['position']  # Sửa 'postion' thành 'position'
                                    match['move_positions'].append(p)
                                user['position'] = match['positions'][selected_positions[-1]-1]['position']
                                user['index'] = match['positions'][selected_positions[-1]]['index']
                                match['dice'] = random_number
                                match['roll'] = 1
                                await self.send_response_to_members(member, match)
                                break
            if remaining_time == 0:
                if turn == t1:
                    # Lấy ra match hiện tại khi hết giờ
                    # Đặt lại giá trị turn trong match
                    turn = t2
                    match['turn_id'] = turn
                    match['roll'] = 0
                    match["request_item_id"] = 0
                    match["move_positions"] = []
                else:
                    # Lấy ra match hiện tại khi hết giờ
                    # Đặt lại giá trị turn trong match
                    turn = t1
                    match['turn_id'] = turn
                    match['roll'] = 0
                    match["request_item_id"] = 0
                    match["move_positions"] = []
                remaining_time = 30


    async def send_response_to_members(self, members, response):
        print(self.clients.__str__())
        for member in members:
            user_id = member['user_id']
            for client in self.clients:
                if client.remote_address[1] == user_id:
                    await client.send(json.dumps(response))
                    break  # Kết thúc vòng lặp sau khi gửi message

    async def update_match(self, item_id, match_id, user_id):
        room = RoomService.get_rooms_by_room_id(match_id)
        member = room['members']
        for match in MatchService.matchs:
            if match.get('match_id') == int(match_id):
                # Kiểm tra xem người dùng hiện tại có nhấn mua hay không
                # Nếu request gửi lên là item trong khi vẫn đang trong lượt thì cho đi, tính toán tiền mua đủ không
                # Cho mua thay thế vị trí cũ luôn
                # Nếu đủ thì cập nhật lại, trừ tiền và gửi match cho toàn bộ user
                if (match["request_item_id"] > 0 and match["request_item_id"] < 5 and user_id == match["turn_id"]):
                    mercenary = Match.mercenary[match["request_item_id"] - 1]
                    for user in match["users"]:
                        if user.get('user_id') == user_id:
                            if ((user.get('gold') - mercenary.get('price')) >= 0):
                                user['gold'] = user.get('gold') - mercenary.get('price')
                                bool = True
                                # Kiểm tra xem vị trí đang đứng có item hay chưa, có thì thay thế uôn
                                for item in match["items"]:
                                    if user.get('index') == item.get('index'):
                                        item['user_id'] = user_id
                                        item['item_id'] = match["request_item_id"]
                                        bool = False
                                        break
                                if bool:
                                    new_item = {
                                        'item_id': user_id,
                                        'attack': mercenary.get('attack'),
                                        'position': match["positions"][user.get('index') - 1]['position'],
                                        'user_id': user_id,
                                        'index': user.get('index')
                                    }
                                    match["items"].append(new_item)
                                await self.send_response_to_members(member, match)
                            break
                    pass
                break








                await self.send_response_to_members(room['members'], match)
                break
        pass
    def random_1_to_6(self):
        return random.randint(1, 6)