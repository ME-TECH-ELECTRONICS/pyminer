# Include libraries
import hashlib
import random
import socket
import time
from _thread import *
from colorama import Fore, Style, Back

# Initialize variables
hash = ""
min = 100000
max = 10000000
diff = str(max)
host = "127.0.0.1"
port = 9090
ThreadCount = 0

# Start the the sever and listen for the client
try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))
server.listen(5)
print("Server started at 127.0.0.1:9090")

# Function for generating hash
def gen_hash(min, max):
    a = random.randrange(min, max)
    Digit = str(a).encode()
    hash = hashlib.sha256(Digit).hexdigest()
    return hash

def threaded_client(client):
    client.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        client.sendall(str.encode(reply))
    client.close()

# Waiting for client to connect
(conn, addr) = server.accept()
print("Accepted a connection request from %s:%s"%(addr[0], addr[1]))

# waithing for Client to send Ready ack
s = conn.recv(1024)
if(s.decode() == "Ready"):
    print("Recived ack")
    time.sleep(1)
    conn.send(diff.encode())
    

    # Generating hash to find
    hashb = gen_hash(min, max)
    print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb )

    # Sending hash to client
    time.sleep(1)
    conn.send(hashb.encode())
    while True:

        # Waiting for client send the hash they found
        hash_stats = conn.recv(1024).decode()
        if("Found hash: " in hash_stats):
            num = hash_stats.split("Found hash: ")
            cnum1 = num[1].replace("b'", "")
            cnum = cnum1.replace("'", "")
            
            # Checking if  client is resending the same hash send by the server 
            if(cnum == hashb):
                print("Wrong hash returned")
                conn.send("BAD SHARES".encode())

                # Generating hash and send after 5s delay
                hashb = gen_hash(min, max)
                time.sleep(5)
                conn.send(hashb.encode())
                print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb)
            else:
                chash = hashlib.sha256(num[1].encode()).hexdigest()
                if (chash == hashb):
                    time.sleep(1)
                    conn.send("GOOD SHARES".encode())
                    hashb = gen_hash(min, max)
                    time.sleep(5)
                    conn.send(hashb.encode())
                    print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb)

            



    
