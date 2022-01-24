# Include libraries
import hashlib
import random
import socket
import time

# Initialize variables
hash = ""
min = 100000
max = 10000000
diff = str(max)

# Start the the sever and listen for the client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1",9090))
server.listen()

# Function for generating hash
def gen_hash(min, max):
    a = random.randrange(min, max)
    Digit = str(a).encode()
    hash = hashlib.sha256(Digit).hexdigest()
    return hash

# Waiting for client to connect
(conn, addr) = server.accept()
print("Accepted a connection request from %s:%s"%(addr[0], addr[1]))

# waithing for Client to send Ready ack
s = conn.recv(1024)
if(s.decode() == "Ready"):
    print("Recived ack")
    time.sleep(1)
    conn.send(diff.encode())
    print("Sending Job: ")

    # Generating hash to find
    hashb = gen_hash(min, max)
    print(hashb)

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
            print(num[1])
            
            # Checking if  client is resending the same hash send by the server 
            if(cnum == hashb):
                print("Wrong hash returned")
                conn.send("BAD SHARES".encode())

                # Generating hash and send after 5s delay
                hashb = gen_hash(min, max)
                time.sleep(5)
                conn.send(hashb.encode())
                print(f'Sending job: {hashb}')
            else:
                chash = hashlib.sha256(num[1].encode()).hexdigest()
                if (chash == hashb):
                    time.sleep(1)
                    conn.send("GOOD SHARES".encode())
                    hashb = gen_hash(min, max)
                    time.sleep(5)
                    conn.send(hashb.encode())
                    print(f'Sending job: {hashb}')

            



    
