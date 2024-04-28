import socket

HOST = '127.0.0.1'  # Server's IP address
PORT = 8888         # Server's port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
    while True:
        msg = input("Client: ")
        s.sendall(bytes(msg, "utf8"))

        if msg == "quit":
            break

        data = s.recv(1024)
        print('Server: ', data.decode("utf8"))

finally:
    s.close()
