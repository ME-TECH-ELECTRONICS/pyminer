import hashlib
import socket
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",9090))
client.send("Ready".encode())
print("Sending ack")
while True:
 ref_hash = client.recv(1024)
 print("Job: ", ref_hash)
 diff = client.recv(1024)
 print("Difficulty: ",diff.decode())
 t1 = time.time()
 for x in range(100000):
  num = str(x).encode()
  my_hash = hashlib.sha256(num).hexdigest().encode()
  if(my_hash == ref_hash):
   t2 = time.time()
   tim = format((t2- t1)*1000, ".3f")
   t_taken = float(tim)
   hashrate = format(x/(t_taken/1000), ".0f")
   client.send(f'Found hash: {x}'.encode())
   ref_hash = ""
   print(f'found hash in {tim}ms')
   print(f'Hashrate: {hashrate}H/s')
   reward = client.recv(1024)
   print(reward.decode())

