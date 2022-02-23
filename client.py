# Including libaries
import hashlib
import socket
import time
from datetime import datetime
from colorama import Fore, Back, Style

# Initialize variables
client = socket.socket()
HOST = "127.0.0.1"
PORT = 9090

# Connecting to the server
try:
    client.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

raw_data = client.recv(1024).decode().split(",")
SERVER_VER = raw_data[0]
diff = int(raw_data[1])
print(f'Connected to {HOST}:{PORT}.\nServer version {SERVER_VER}. \nHappy Minning :)') 

while True:
    # Sending Ready ack to sever
    client.send("JOB".encode())
    # Requesting the difficulty of hash
    dificulty = diff

    # Requesting the ref hash from server
    ref_hash = client.recv(1024)
    t1 = time.time()

    # Starting the mining process
    for x in range(dificulty):
        num = str(x).encode()
        my_hash = hashlib.sha256(num).hexdigest().encode()

        #checking if the hash matches that of sever 
        if(my_hash == ref_hash):
            t2 = time.time()
            tim = format((t2- t1), ".3f")
            t_taken = float(tim)
            h = x/t_taken
            hashrate = format(h/1000, ".0f")
            # Sending the hash found by the client to server
            client.send(f'Found hash: {x}'.encode())
            ref_hash = ""
            reward = client.recv(1024).decode()
            if(reward == "GOOD SHARES"):
                print(Fore.WHITE + datetime.now().strftime(Style.DIM + "%H:%M:%S ") + Style.BRIGHT + Back.GREEN + Fore.BLACK +'SYS0' + Style.RESET_ALL + Fore.GREEN + " - ⛏ Accepted - " + Style.RESET_ALL + tim + "s - " + Fore.BLUE + hashrate + "KH/s" + Style.RESET_ALL)
            else:
                print(reward)
