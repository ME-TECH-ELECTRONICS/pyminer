import socket
import time
import signal
import sys

stats = socket.socket()
HOST = "127.0.0.1"
PORT = 9090

try:
    stats.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    stats.send("END".encode())
    time.sleep(5)
    sys.exit(0)

#stats.send("STATUS".encode())
#n = stats.recv(1024)

while True:
    stats.send("STATUS".encode())
    print("Fetching data...")
    data = stats.recv(1024).decode().split(",")
    print(data)
    SERVER_VER = data[0]
    CLIENT_CONN = data[1]
    print(f'Server IP: {HOST}:{PORT}\nServer version: {SERVER_VER}\nClient Connected : {CLIENT_CONN}')
    time.sleep(5)
    signal.signal(signal.SIGINT, signal_handler)
