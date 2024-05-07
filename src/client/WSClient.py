import json
import socket

class Client:
    state = 0
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def send_request(self, data):
        while True:
            data = {
                'object': 'map',
                'operation': "update",
                'json': "city"
            }
            if (Client.state == 1):
                json_data = json.dumps(data)
                self.client_socket.sendall(bytes(json_data, 'utf-8'))
                response = self.client_socket.recv(1024)
                print(response.decode('utf-8'))
                Client.state = 0
    def close_connection(self):
        self.client_socket.close()

client = Client('127.0.0.1', 10000)
client.send_request()
client.close_connection()