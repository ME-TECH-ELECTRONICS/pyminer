############################################
""" Including libaries """
############################################
import hashlib
import socket
import time
import signal
import sys
from datetime import datetime
from colorama import Fore, Back, Style

############################################
""" Initialize variables """
############################################
client = socket.socket()
HOST = "127.0.0.1"
PORT = 9090
diff_lvl = input("Enter difficulty level: ")

############################################
"""Connecting to the server"""
############################################
try:
    client.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

############################################
    ''' Ctrl C event handler'''
############################################
def signal_handler(sig, frame):
    print(Fore.YELLOW + "Exiting miner....Bye!" + Style.RESET_ALL)
    client.send("END".encode())
    time.sleep(5)
    sys.exit(0)

raw_data = client.recv(1024).decode()
SERVER_VER = raw_data
print(f'Connected to {HOST}:{PORT}.\nServer version {SERVER_VER}. \nHappy Minning :)') 

############################################
''' Main program '''
############################################
while True:
    signal.signal(signal.SIGINT, signal_handler)
    client.send("JOB".encode())
    difficulty = diff

    # Requesting the ref hash from server
    ref_hash = client.recv(1024)
    t1 = time.time()

    # Starting the mining process
    for x in range(difficulty):
        num = str(x).encode()
        my_hash = hashlib.sha256(num).hexdigest().encode()

        #checking if the hash matches that of sever 
        if(my_hash == ref_hash):
            t2 = time.time()
            tim = format((t2- t1), ".3f")
            t_taken = float(tim)
            h = x/t_taken
            hashrate = format(h/1000, ".0f")
            client.send(f'Found hash: {x}'.encode())
            reward = client.recv(1024).decode()
            if(reward == "GOOD SHARES"):
                print(Fore.WHITE 
                      + datetime.now().strftime(Style.DIM + "%H:%M:%S ") 
                      + Style.BRIGHT + Back.GREEN + Fore.BLACK +'SYS0' 
                      + Style.RESET_ALL + " - " + Fore.GREEN + "⛏ Accepted" 
                      + Style.RESET_ALL + " - " + tim + "s - " 
                      + Fore.BLUE + hashrate + "KH/s" 
                      + Style.RESET_ALL
                      + " - ⚙ diff: "
                      + str(diff))
            elif(reward == "BAD SHARES"):
                print(Fore.WHITE 
                      + datetime.now().strftime(Style.DIM + "%H:%M:%S ") 
                      + Style.BRIGHT + Back.GREEN + Fore.BLACK +'SYS0' 
                      + Style.RESET_ALL + Fore.RED + " - ⛏ Rejected - " 
                      + Style.RESET_ALL + tim + "s - " 
                      + Fore.BLUE + hashrate + "KH/s" 
                      + Style.RESET_ALL
                      + "⚙ diff: "
                      + str(diff))
