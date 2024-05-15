import json

from src.server.sevice.UserService import UserService


class RoomService:
    rooms = []

    def __init__(self):
        self.client = None
        self.clients = None
        pass

    async def process_request(self, request, user_id, client, clients):
        self.client = client
        self.clients = clients
        self.user_id = user_id
        action = request['action']
        if action == 'get_all':
            await self.get_all_rooms()
        elif action == 'create':
            await self.create_room(self.user_id)
        elif action == 'join':
            room_id = request.get('room_id')
            await self.join_room(user_id, room_id)
        elif action == 'get_by_room_id':
            room_id = request.get('room_id')
            await self.get_rooms_by_room_id(room_id)
        elif action == 'leave':
            room_id = request.get('room_id')
            await self.leave_room(user_id, room_id)
        elif action == 'delete':
            await self.delete(user_id)
        else:
            # Nếu yêu cầu không phù hợp với các điều kiện trên, trả về phản hồi lỗi
            response = {'status': 'error', 'message': 'Invalid request'}
            await self.client.send(json.dumps(response))

    async def get_all_rooms(self):
        # Xử lý yêu cầu lấy tất cả các phòng
        # Ví dụ: Trả về danh sách các phòng
        response = {'status': 'success', 'message': 'All rooms retrieved', 'rooms': RoomService.rooms}
        await self.client.send(json.dumps(response))

    async def create_room(self, room_id):
        # Kiểm tra xem phòng đã tồn tại chưa
        if self.room_exists(room_id):
            response = {'status': 'error', 'message': f'Room already exists for room_id {room_id}'}
            await self.client.send(json.dumps(response))
        else:
            user = UserService.get_user_by_id(room_id)
            if user:
                # Tạo phòng mới và thêm vào danh sách các phòng
                room = {'room_id': room_id, 'status': 'active',
                        'members': [{'user_id': room_id, 'user_name': user['user_name'], 'role': 'master'}]}
                RoomService.rooms.append(room)
                response = {'status': 'success', 'message': f'Room created for room_id {room_id}'}
                await self.client.send(json.dumps(response))
            else:
                response = {'status': 'error', 'message': f'User not found for user_id {room_id}'}
                await self.client.send(json.dumps(response))

    async def join_room(self, user_id, room_id):
        # Xử lý yêu cầu tham gia phòng với chủ sở hữu là `room_id`
        # Ví dụ: Tìm phòng có chủ sở hữu là `room_id` và thực hiện các hành động liên quan
        user = UserService.get_user_by_id(user_id)
        room = RoomService.get_rooms_by_room_id(room_id)

        if room and 'members' in room and user:
            is_member = False
            for member in room['members']:
                if member['user_id'] == user_id:
                    is_member = True
                    break

            if not is_member:
                room['members'].append({'user_id': user_id, 'user_name': user['user_name'], 'role': 'member'})
                response = {'status': 'success', 'message': f'Joined room for owner {room_id}',
                            'data': RoomService.rooms[:]}

                await self.send_response_to_members(room['members'], response)
            else:
                response = {'status': 'success', 'message': f'User is already a member of the room {room_id}'}
                await self.client.send(json.dumps(response))
        else:
            response = {'status': 'error', 'message': f'Room or user not found for owner {room_id}'}
            await self.client.send(json.dumps(response))

    async def send_response_to_members(self, members, response):
        print(self.clients.__str__())
        for member in members:
            user_id = member['user_id']
            for client in self.clients:
                if client.remote_address[1].__str__() == user_id.__str__():
                    await client.send(json.dumps(response))
                    break  # Kết thúc vòng lặp sau khi gửi message

    def get_rooms_by_room_id(room_id):
        # Xử lý yêu cầu lấy phòng với `room_id`
        # Ví dụ: Tìm và trả về phòng cụ thể với `room_id`
        for room in RoomService.rooms:
            print(room_id.__str__() +"vs" + room['room_id'].__str__())
            if room_id.__str__() == room['room_id'].__str__():
                return room
        return None

    def room_exists(self, room_id):
        # Kiểm tra xem phòng đã tồn tại với chủ sở hữu là `room_id` hay chưa
        for room in RoomService.rooms:
            if room['room_id'] == room_id:
                return True
        return False

    async def delete(self, room_id):
        roomsss = RoomService.get_rooms_by_room_id(room_id)
        # Xóa phòng với chủ sở hữu là `room_id` khỏi danh sách `rooms`
        deleted_rooms = [room for room in self.rooms if room['room_id'] == room_id]
        RoomService.rooms = [room for room in self.rooms if room['room_id'] != room_id]
        if deleted_rooms:
            response = {'status_delete': 1}
        else:
            response = {'status_delete': 1}
        await self.send_response_to_members(roomsss['members'], response)

    async def hard_delete(self, room_id):
        # Xóa phòng với chủ sở hữu là `room_id` khỏi danh sách `rooms`
        deleted_rooms = [room for room in self.rooms if room['room_id'] == room_id]
        RoomService.rooms = [room for room in self.rooms if room['room_id'] != room_id]

    async def leave_room(self, user_id, room_id):
        roomsss = RoomService.get_rooms_by_room_id(room_id)
        for room in RoomService.rooms:
            if room['room_id'].__str__() == room_id.__str__():
                for member in room['members']:
                    if member['user_id'].__str__() == user_id.__str__():
                        room['members'].remove(member)  # Xóa người dùng khỏi danh sách
                        response = {'status_leave': 1}
                        await self.client.send(json.dumps(response))
                        await self.send_response_to_members(roomsss['members'], response)
                        break
        pass
