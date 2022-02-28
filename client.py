############################################
###########  Importing libaries  ###########
############################################
import hashlib
import socket
import time
import signal
from  sys import exit
from os import execl, mkdir
from datetime import datetime
from colorama import Fore, Back, Style
from pathlib import Path
from configparser import ConfigParser

############################################
######  Initialize global variables  #######
############################################
client = socket.socket()
configparser = ConfigParser()
HOST = "127.0.0.1"
PORT = 9090

############################################
#########  Default miner config  ###########
############################################
class SETTINGS:
    DATA_DIR = "Miner-cfg"
    CONFIG_FILE = "/config.cfg"
    SOC_TIMEOUT = 15

#############################################
# Function for creating/loading config file #
#############################################
def load_cfg():
    if not Path(SETTINGS.DATA_DIR).is_dir():
        mkdir(SETTINGS.DATA_DIR)

    if not Path(SETTINGS.DATA_DIR + SETTINGS.CONFIG_FILE).is_file():
        print("Basic Config file setup")
        username = input("Enter the username: ")
        print("Available options: LOW, MEDIUM, HIGH")
        diff_lvl = input("Enter the difficulty: ")
        rig_id = input("Enter a name for the Rig ")
        
        configparser["PC Miner"] = {
            "username":    username,
            "difficulty":  diff_lvl,
            "rid_id":      rig_id,
            "soc_timeout": SETTINGS.SOC_TIMEOUT}

        with open(SETTINGS.DATA_DIR + SETTINGS.CONFIG_FILE, "w") as configfile:
                configparser.write(configfile)

    configparser.read(SETTINGS.DATA_DIR+ SETTINGS.CONFIG_FILE)
    return configparser["PC Miner"]

############################################
###########  Load Config file  #############
############################################
config = load_cfg()
username = config["username"]
diff_lvl = config["difficulty"]
rig_id = config["rid_id"]
############################################
########  Connecting to the server  ########
############################################
try:
    client.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

############################################
########    Ctrl C event handler   #########
############################################
def signal_handler(sig, frame):
    client.send("END".encode())
    print(Fore.YELLOW + "Exiting miner....Bye!" + Style.RESET_ALL)
    time.sleep(5)
    exit(0)

raw_data = client.recv(1024).decode()
SERVER_VER = raw_data
print(Fore.BLACK + Back.CYAN + "INET" +Style.RESET_ALL + f' Connected to {HOST}:{PORT}.\n'+ Fore.BLACK + Back.CYAN + "INET" +Style.RESET_ALL + f' Server version {SERVER_VER}.') 
client.send(diff_lvl.encode())
diff = client.recv(256).decode()
print(Fore.BLACK + Back.CYAN + "INET" +Style.RESET_ALL + f' Difficulty set to {diff}.')

############################################
''' Main program '''
############################################
while (1):
    signal.signal(signal.SIGINT, signal_handler)
    client.send('JOB'.encode())
    ref_hash = client.recv(1024)
    t1 = time.time()

    # Starting the mining process
    for x in range(int(diff)):
        num = str(x).encode()
        my_hash = hashlib.sha256(num).hexdigest().encode()

        #checking if the hash matches that of sever 
        if(my_hash == ref_hash):
            t2 = time.time()
            tim = format((t2- t1), ".3f")
            t_taken = float(tim)
            h = x/t_taken
            hashrate = format(h/1000, ".0f")
            client.send(f'Found nonce: {x}'.encode())
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
                print(Fore.WHITE 
                    + datetime.now().strftime(Style.DIM + "%H:%M:%S ") 
                    + Style.BRIGHT + Back.CYAN + Fore.BLACK +'INET' 
                    + Style.RESET_ALL + " - " + "Recieved JOB" + Style.RESET_ALL)

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

