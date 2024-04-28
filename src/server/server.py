import socket

HOST = '127.0.0.1'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)

while True:
    client, addr = s.accept()

    try:
        print('Connected by', addr)
        while True:
            data = client.recv(1024)
            if not data:  # Check if the client has disconnected
                print("Client disconnected")
                break

            str_data = data.decode("utf8")
            print("Client: " + str_data)

            msg = input("Server: ")
            client.sendall(bytes(msg, "utf8"))

    finally:
        client.close()

s.close()
