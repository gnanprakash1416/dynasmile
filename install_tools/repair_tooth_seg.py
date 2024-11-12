import paramiko

from forward import forward_tunnel

import time

import signal

import sys

import threading

import os

import argparse
# create
parser = argparse.ArgumentParser(description='Please enter your server. For instance:ec2-54-175-40-110.compute-1.amazonaws.com')
# add
parser.add_argument('--server', type=str, help='Type the address of the server', required=True)
# parse
args = parser.parse_args()

hostname = args.server

port = 22

username = 'ec2-user'

current_path=os.path.abspath(__file__)
current_folder=os.path.dirname(current_path)

key_file_path = os.path.join(current_folder,'key.pem') 

# create ssh client

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# function that processes the signal

def signal_handler(sig, frame):

    print('\nclosing ssh connection...')

    ssh_client.close()

    sys.exit(0)

# register

signal.signal(signal.SIGINT, signal_handler)

try:

    # load key

    private_key = paramiko.RSAKey.from_private_key_file(key_file_path)

    # connect to server

    ssh_client.connect(hostname, port=port, username=username, pkey=private_key)

    print("SSH successfully connected，port forwarding 8888...")


    forward_thread = threading.Thread(target=forward_tunnel, args=(8888, 'localhost', 8888, ssh_client.get_transport()))

    forward_thread.daemon = True # 

    forward_thread.start()

    print("press Ctrl+C to close connection。")

    shell=ssh_client.invoke_shell()

    time.sleep(1)

    shell.send('conda activate rtmdet-sam'+'\n')

    time.sleep(1)

    output=shell.recv(10000).decode("utf-8")

    print(output)

    shell.send('jupyter-lab') #screen to keep the sh running, or the fee cannot be controlled.

    time.sleep(2)

    output=shell.recv(10000).decode("utf-8")

    print(output)

    while True:

        command = input("Type /command (type 'exit' to exit): ")

        if command.lower() == 'exit':

            break

        # 

        #shell.send(command+'\n')

        time.sleep(1)

        output=shell.recv(10000).decode("utf-8")

        #print("shuchu:")

        print(output)


except Exception as e:

    print(f"error encountered: {e}")

finally:


    if ssh_client.get_transport() is not None:

        ssh_client.close()