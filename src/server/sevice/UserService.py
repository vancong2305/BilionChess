class UserService:
    users = []

    def __init__(self):
        self.clients = None
        pass

    def process_request(self, request, user_id, clients):
        self.clients = clients
        self.user_id = user_id
        action = request['action']
        if action == 'create':
            user_name = request.get('user_name')
            return self.create_user(user_id, user_name)
        elif action == 'get_all':
            return self.get_all()
        # elif action == 'delete':
        #     user_id = request.get('user_id')
        #     return self.delete(user_id)
        # Nếu yêu cầu không phù hợp với các điều kiện trên, trả về phản hồi lỗi
        response = {'status': 'error', 'message': 'Invalid request'}
        return response
    def create_user(self, user_id, user_name):
        # Kiểm tra xem user đã tồn tại chưa
        # if self.user_exists(user_id):
        #     response = {'status': 'error', 'message': f'user already exists for user_id {user_id}'}
        # else:
        #     # Tạo user mới và thêm vào danh sách các user
        #     user = {'user_id': user_id, 'user_name' : user_name, 'status': 'active'}
        #     UserService.users.append(user)
        #     response = {'status': 'success', 'message': f'user created for user_id {user_id}'}
        # return response

        user = {'user_id': user_id, 'user_name': user_name, 'status': 'active'}
        UserService.users.append(user)
        response = {'status': 'success', 'message': f'user created for user_id {user_id}'}
        return response

    def user_exists(self, user_id):
        # Kiểm tra xem user đã tồn tại với chủ sở hữu là `user_id` hay chưa
        for user in UserService.users:
            if user['user_id'] == user_id:
                return True
        return False

    async def delete(self, user_id):
        # Xóa user có `user_id` ra khỏi danh sách `users`
        deleted_users = [user for user in self.users if user['user_id'] == user_id]
        UserService.users = [user for user in self.users if user['user_id'] != user_id]

        if deleted_users:
            response = {'status': 'success', 'message': f'users deleted for user_id {user_id}',
                        'deleted_users': deleted_users}
        else:
            response = {'status': 'error', 'message': f'No users found for user_id {user_id}'}


    def get_user_by_id(user_id):
        # Tìm người dùng dựa trên user_id
        for user in UserService.users:
            if user['user_id'] == user_id:
                return user
        return None

    def get_all(self):
        response = {'status': 'success', 'message': 'All user retrieved', 'users': UserService.users}
        return response