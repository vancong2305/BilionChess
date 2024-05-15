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
        # Tạo task riêng để đếm ngược 20 giây
        self.timer_task = asyncio.create_task(self.start_match(room['members'], user_id, turn_id_1, turn_id_2))
    async def start_match(self, member, user_id, turn_id_1, turn_id_2):
        remaining_time = 20
        uid = user_id
        t1 = turn_id_1
        t2 = turn_id_2
        turn = t1
        boolean_check = True
        char_state = 1
        while boolean_check:
            await asyncio.sleep(1)
            response = {
                "remaining_time": remaining_time
            }
            await self.send_response_to_members(member, response)
            remaining_time -= 1
            boolchk = True
            for match in MatchService.matchs:
                if match.get('match_id') == uid:
                    boolchk = False
                    # Quay xúc sắc và gửi lại response cho user nếu lượt này chưa roll, cập nhật lại vị trí của user
                    if (match["roll"] == 0):
                        match['turn_id'] = turn
                        match['char_id'] = char_state
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
                                user['index'] = match['positions'][selected_positions[-1]-1]['index']
                                match['dice'] = random_number
                                match['roll'] = 1

                                # Trừ máu nếu đi vào ô của đối thủ
                                # Nếu item là 1 trừ máu luôn bất kể ai sở hữu nếu đi vào index đó
                                if len(match['items'])>0:
                                    for item in match['items']:
                                        if item['user_id'] !=  match['turn_id']:
                                            if item['item_id'] == 2 and user.get('index') == item.get('index'):
                                                user['hp'] = user.get('hp') - item.get('attack')
                                            if item['item_id'] == 3 and user.get('index') == item.get('index'):
                                                user['hp'] = user.get('hp') - item.get('attack')
                                            if item['item_id'] ==4 and user.get('index') == item.get('index'):
                                                user['hp'] = user.get('hp') - item.get('attack')
                                        if item['item_id'] == 1 and user.get('index') == item.get('index'):
                                            user['hp'] = user.get('hp') - item.get('attack')
                                        if user['hp'] <= 0:
                                            user['hp'] = 0

                                # Kiểm tra người chiến thắng
                                # Kiểm tra hp
                                if user['hp'] <= 0:
                                    # Nếu lượt hiện tại của người thứ nhất thì người thứ 2 thắng và ngược lại
                                    if user['user_id'] == t1:
                                        match['winner'] = int(t2)
                                        match['reason_win'] = "Bạn thắng! Thương trường đầy âm mưu biến cố. Dùng não, dùng tiền đều phải đúng chỗ. Đối thủ không còn đủ sức khoẻ để chèo trống trước những toan tính hiểm hóc của bạn!"
                                        match['reason_lose'] = "Bạn thua vì không còn sức khoẻ để chống lại toan tính của đối thủ. Xin chia buồn, lần sau cố gắng nhé!"
                                    else:
                                        match['winner'] = int(t1)
                                        match['reason_win'] = "Bạn thắng! Thương trường đầy âm mưu biến cố. Dùng não, dùng tiền đều phải đúng chỗ. Đối thủ không còn đủ sức khoẻ để chèo trống trước những toan tính hiểm hóc của bạn!"
                                        match['reason_lose'] = "Bạn thua vì không còn sức khoẻ để chống lại toan tính của đối thủ. Xin chia buồn, lần sau cố gắng nhé!"
                                # Kiểm tra số lượng tiền
                                if user['gold'] >= 6000 and user['hp'] >= 0:
                                    match['winner'] = user['user_id']
                                    match['reason_win'] = "Bạn thắng! Phú khả địch quốc huống chi là đối thủ. Bạn là một thương gia giỏi, kiếm tiền khủng quá, đối thủ cũng phải chào thua!"
                                    match['reason_lose'] = "Bạn thua vì không còn sức khoẻ để chống lại toan tính của đối thủ. Xin chia buồn, lần sau cố gắng nhé!"
                                await self.send_response_to_members(member, match)
                                # Xoá trận sau khi thắng
                                # Giải phóng task cho trận này
                                if match['winner'] != 0:
                                    boolean_check = False
                                break
            for match in MatchService.matchs:
                if match["match_id"] == t1 and boolean_check == 0:
                    MatchService.matchs.remove(match)  # Xóa phần tử
            if boolchk:
                for match in MatchService.matchs:
                    if match["match_id"] == t1 and boolean_check == 0:
                        MatchService.matchs.remove(match)  # Xóa phần tử
                boolean_check = False
            if remaining_time == 0:
                if turn == t1:
                    # Lấy ra match hiện tại khi hết giờ
                    # Đặt lại giá trị turn trong match
                    turn = t2
                    for match in MatchService.matchs:
                        if match.get('match_id') == uid:
                            match['turn_id'] = turn
                            match['roll'] = 0
                            char_state = 2
                            match["request_item_id"] = 0
                            match["request_status"] = 0
                            match["move_positions"] = []
                else:
                    # Lấy ra match hiện tại khi hết giờ
                    # Đặt lại giá trị turn trong match
                    turn = t1
                    for match in MatchService.matchs:
                        if match.get('match_id') == uid:
                            match['turn_id'] = turn
                            match['roll'] = 0
                            char_state = 1
                            match["request_item_id"] = 0
                            match["request_status"] = 0
                            match["move_positions"] = []
                remaining_time = 20


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
                if match["request_status"] == 0 and item_id > 0 and item_id < 5 and int(user_id) == match["turn_id"]:
                    mercenary = Match.mercenary[item_id - 1]
                    for user in match["users"]:
                        if user.get('user_id') == int(user_id):
                            if (user.get('gold') - mercenary.get('price')) >= 0:
                                user['gold'] = user.get('gold') - mercenary.get('price')
                                bool = True
                                match["request_status"] = 1
                                # Kiểm tra xem vị trí đang đứng có item hay chưa, có thì thay thế uôn
                                for item in match["items"]:
                                    if user.get('index') == item.get('index'):
                                        item['user_id'] = int(user_id)
                                        item['item_id'] = item_id
                                        if int(user_id) != int(match_id):
                                            item['color'] = 2
                                        else:
                                            item['color'] = 1
                                        bool = False
                                        break
                                if bool:
                                    numcolor = 1
                                    if int(user_id) != int(match_id):
                                        numcolor = 2
                                    else:
                                        numcolor = 1
                                    new_item = {
                                        'user_id': int(user_id),
                                        'item_id': item_id,
                                        'attack': mercenary.get('attack'),
                                        'position': match["positions"][user.get('index') - 1]['position'],
                                        'index': user.get('index'),
                                        'color': numcolor
                                    }
                                    match["items"].append(new_item)

                                await self.send_response_to_members(member, match)
            break
    def random_1_to_6(self):
        return random.randint(1, 6)