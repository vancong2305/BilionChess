import json
import socket

HOST = '127.0.0.1'  # Server's IP address
PORT = 9999         # Server's port

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while True:
            # Get user input and convert to JSON
            msg = input("Client: ")

            # Send data to server
            s.sendall(msg.encode("utf8"))

            # Check for quit command
            if msg == "quit":
                exit(0)
                break

            # Receive data from server
            data = s.recv(1024)
            print('Server: ', data.decode("utf8"))

    except ConnectionResetError:
        print("Connection to server was unexpectedly closed. Retrying...")

    finally:
        s.close()
        print("Client disconnected.")
