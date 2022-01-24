# Including libaries
import hashlib
import socket
import time

# Connecting to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",9090))

# Sending Ready ack to sever
client.send("Ready".encode())
print("Sending ack")

# Requesting the difficulty of hash
diff = client.recv(1024)
print("Difficulty: ",diff.decode())
dificulty = int(diff.decode())
while True:

    # Requesting the ref hash from server
    ref_hash = client.recv(1024)
    print("\nJob: ", ref_hash)
    t1 = time.time()

    # Starting the mining process
    for x in range(dificulty):
        num = str(x).encode()
        my_hash = hashlib.sha256(num).hexdigest().encode()

        #checking if the hash matches that of sever 
        if(my_hash == ref_hash):
            t2 = time.time()
            tim = format((t2- t1)*1000, ".3f")
            t_taken = float(tim)
            h = x/(t_taken/1000)
            hashrate = format(h/1000, ".0f")
            # Sending the hash found by the client to server
            client.send(f'Found hash: {x}'.encode())
            ref_hash = ""
            print(f'found hash in {tim}ms')
            print(f'Hashrate: {hashrate}KH/s')
            reward = client.recv(1024)
            print(reward.decode())

