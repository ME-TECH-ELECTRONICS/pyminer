import socket
import time

stats = socket.socket()
HOST = "127.0.0.1"
PORT = 9090

try:
    stats.connect((HOST, PORT))
except socket.error as e:
    print(str(e))


while True:
    stats.send("status".encode())
    data = stats.recv(4098).decode().split(",")
    print(data)
    SERVER_IP = data[0]
    SERVER_PORT = data[1]
    SERVER_VER = data[3]
    CLIENT_CONN = data[1]
    print(f'Server IP: {SERVER_IP}:{SERVER_PORT}\nServer version: {SERVER_VER}\nClient Connected : {CLIENT_CONN}')
    time.sleep(10)
