# Include libraries
import hashlib
import random
import socket
import time

# Initialize variables
hash = ""
diff = "100000"

# Start the the sever and listen for the client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1",9090))
server.listen()

# Function for generating hash
def gen_hash(hash):
    a = random.randrange(10000, 100000)
    Digit = str(a).encode()
    hash = hashlib.sha256(Digit).hexdigest()
    return hash

(clientConnected, clientAddress) = server.accept()
print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))
s = clientConnected.recv(1024)
stats = s.decode()
if(stats == "Ready"):
    print("Recived ack, sending job")
    hashb = gen_hash(hash)
    print(hashb)
    clientConnected.send(hashb.encode())
    time.sleep(1)
    clientConnected.send(diff.encode())
    while(True):
        hash_stats = clientConnected.recv(1024).decode()
        if("Found hash: " in hash_stats):
            num = hash_stats.split("Found hash: ")
            cnum1 = num[1].replace("b'", "")
            cnum = cnum1.replace("'", "")
            print(num[1])
            if(cnum == hashb):
                print("Wrong hash returned")
                clientConnected.send("BAD SHARES".encode())
                hashb = gen_hash(hash)
                time.sleep(5)
                clientConnected.send(hashb.encode())
                print(f'Sending job: {hashb}')
            else:
                chash = hashlib.sha256(num[1].encode()).hexdigest()
                if (chash == hashb):
                    clientConnected.send("GOOD SHARES".encode())
                    hashb = gen_hash(hash)
                    time.sleep(5)
                    clientConnected.send(hashb.encode())
                    time.sleep(3)
                    clientConnected.send(str(diff).encode())
                    print(f'Sending job: {hashb}')

            



    
