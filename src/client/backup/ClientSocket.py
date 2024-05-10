import json
import socket
import threading


class Client:
    client = None
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, data):
        if self.client_socket is None:
            raise Exception('Client is not connected to the server.')

        json_data = json.dumps(data)
        self.client_socket.sendall(bytes(json_data, 'utf-8'))
        response = self.client_socket.recv(1024)
        return response.decode('utf-8')

    def receive_message(self):
        if self.client_socket is None:
            raise Exception('Client is not connected to the server.')

        while True:
            response = self.client_socket.recv(1024)
            print(response.decode('utf-8'))

    def close_connection(self):
        if self.client_socket is not None:
            self.client_socket.close()
            self.client_socket = None

# # Gửi yêu cầu và nhận phản hồi từ server
# data = {
#     'object': 'map',
#     'operation': 'update',
#     'json': 'city'
# }
# # Lắng nghe tin nhắn từ server (chạy trong một thread riêng)
# threading.Thread(target=client.receive_message).start()
