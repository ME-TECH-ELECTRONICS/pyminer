# Include libraries
import hashlib

import random
import socket
import time
from _thread import *
from colorama import Fore, Style, Back

# Initialize variables
Test ="" 
hash = ""
min = 100000
max = 10000000
diff = str(max)
HOST = "127.0.0.1"
PORT = 9090
thread_count = 0
SERVER_VER = "v1.0"

# Start the the sever and listen for the client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9090))
server.listen(10)
print(Fore.GREEN + "Server started at 127.0.0.1:9090" + Style.RESET_ALL)

# Function for generating hash
def gen_hash(min, max):
    a = random.randrange(min, max)
    Digit = str(a).encode()
    hash = hashlib.sha256(Digit).hexdigest()
    return hash

    
def client_thread(client, addr, IP):
    while True:
        s = client.recv(1024)
        if (s.decode() == "STATUS"):
            time.sleep(2)
            client.send(f'{SERVER_VER},{IPS}'.encode())
    
        elif (s.decode() == "READY"):
            print(addr + " - Recived ack")
        
            # Generating hash to find
            hashb = gen_hash(min, max)
            print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb )

            # Sending hash to client
            time.sleep(1)
            client.send(hashb.encode())

            # Waiting for client send the hash they found
            hash_stats = client.recv(1024).decode()
            if("Found hash: " in hash_stats):
                num = hash_stats.split("Found hash: ")
                cnum1 = num[1].replace("b'", "")
                cnum = cnum1.replace("'", "")
            
                # Checking if  client is resending the same hash send by the server 
                if(cnum == hashb):
                    print("Wrong hash returned")
                    client.send("BAD SHARES".encode())

                    # Generating hash and send after 5s delay
                    hashb = gen_hash(min, max)
                    time.sleep(5)
                    client.send(hashb.encode())
                    print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb)
                else:
                    chash = hashlib.sha256(num[1].encode()).hexdigest()
                    if (chash == hashb):
                        time.sleep(1)
                        client.send("GOOD SHARES".encode())
                        hashb = gen_hash(min, max)
                        time.sleep(5)
                        client.send(hashb.encode())
                        print(Fore.GREEN + "Sending Job: " + Style.RESET_ALL + hashb)
        elif (s.decode() == "END"):
            client.close()
            print(Fore.RED + "Client disconnected" + Style.RESET_ALL)
            exit()
        

if __name__ == '__main__':
    while True:
        client, address = server.accept()
        client.send(f'{SERVER_VER},{diff}'.encode())
        thread_count += 1
        IPS = IPS.append(str(address[1]))
        c = len(IPS)
        C_IP = address[0] + ":" + str(address[1])
        print(str(address))
        print('Connected to: ' + address[0] + ':' + str(address[1]) )
        start_new_thread(client_thread, (client, C_IP, c ))
        
 


    
