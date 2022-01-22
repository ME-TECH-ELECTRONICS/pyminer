import hashlib
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.42.129",9090))
client.send("Ready".encode())
print("Sending ack")
while True:
    
    ref_hash = client.recv(1024)
    print("ref hash: ", ref_hash)
    t1 = time.time()
    for x in range(100000):
        num = str(x).encode()
        my_hash = hashlib.sha256(num).hexdigest().encode()
        if(my_hash == ref_hash):
            t2 = time.time()
            t = format((t2- t1)*1000, ".3f")
            client.send(f'Found hash: {x}'.encode())
            ref_hash = ""
            print(f'found hash in {t}ms')
            reward = client.recv(1024)
            print(reward.decode())

