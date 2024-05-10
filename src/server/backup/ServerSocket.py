import signal
import threading
import json
import socket
import time

from src.server.sevice.RoomService import RoomService


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_running = True
        self.clients = []
        self.server_socket = None
        self.roomService = RoomService()

    def handle_client(self, client_socket):
        try:
            print('Kết nối từ', client_socket.getpeername())
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("Client ngắt kết nối")
                    break
                json_data = data.decode("utf8")
                print(json_data)
                # Xử lý dữ liệu JSON nhận được
                try:
                    received_data = json.loads(json_data)
                    object = received_data['object']
                    operation = received_data['operation']
                    data = received_data['data']
                    if (object == "room"):
                        if operation == 'join':
                            self.roomService.add(received_data)
                        elif operation == 'create':
                            self.roomService.create(received_data)
                        elif operation == 'get':
                            self.roomService.get(received_data)
                        elif operation == 'start':
                            self.roomService.start(received_data)
                    msg = f"Nhận đối tượng JSON thành công: Tên: {object}, Tuổi: {operation}, Thành phố: {data}"
                    client_socket.sendall(bytes(msg, "utf8"))
                except (json.JSONDecodeError, KeyError) as e:
                    # Xử lý JSON không hợp lệ hoặc thiếu trường dữ liệu một cách graceful
                    print(f"Lỗi xử lý JSON: {e}")
                    msg = "Đối tượng JSON không hợp lệ"
                    client_socket.sendall(bytes(msg, "utf8"))

        finally:
            # Đảm bảo socket của client được đóng ngay cả khi có ngoại lệ xảy ra
            client_socket.close()
            self.clients.remove(client_socket)

    def send_message_to_room(self, room, message):
        if room in self.clients:
            room_clients = self.clients[room]
            for client_socket in room_clients:
                try:
                    client_socket.sendall(bytes(message, "utf8"))
                except Exception as e:
                    print(f"Lỗi gửi tin nhắn tới client: {e}")
        else:
            print(f"Phòng {room} không tồn tại")

    def send_hello_message(self):
        while self.is_running:
            time.sleep(5)  # Chờ 30 giây
            hello_msg = "Xin chào từ server!"
            for client_socket in self.clients:
                try:
                    client_socket.sendall(bytes(hello_msg, "utf8"))
                except Exception as e:
                    print(f"Lỗi gửi tin nhắn tới client: {e}")

    def run(self):
        signal.signal(signal.SIGINT, lambda signal, frame: self.stop_server())

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server_socket:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(20)

            print('Server lắng nghe trên cổng', self.port)
            threading.Thread(target=self.send_hello_message).start()

            while self.is_running:
                client, addr = self.server_socket.accept()
                self.clients.append(client)
                threading.Thread(target=self.handle_client, args=(client,)).start()

            print('Server đã dừng')

    def stop_server(self):
        self.is_running = False

# Sử dụng lớp Server
server = Server('127.0.0.1', 8800)
server.run()