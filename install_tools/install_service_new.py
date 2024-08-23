import paramiko
import time
import paramiko
import signal
import sys
import threading
import os
from library.another import manage_item
from library.forward import forward_tunnel
import subprocess

current_path=os.path.abspath(__file__)
current_folder=os.path.dirname(current_path)
parent_folder=os.path.dirname(current_folder)
upper_folder=os.path.dirname(parent_folder)

server=manage_item(os.path.join(parent_folder,'client','software','library','server.json'),"server")
if server==2 or server==3:
    server=manage_item(os.path.join(parent_folder,'client','library','server.json'),"server")

python_path=os.path.join(parent_folder,'venv','Scripts','python.exe')

hostname = server

port = 22

username = 'ec2-user'

key_file_path = os.path.join(parent_folder,'client','software','library','key.pem') 

private_key = paramiko.RSAKey.from_private_key_file(key_file_path)

path_to_file=os.path.join(parent_folder,"server","service.zip")

path_to_decompress=os.path.join(parent_folder,"server","decompress_service.py")
# 创建SSH客户端
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname, port=port, username=username, pkey=private_key)
# 定义一个函数来执行命令并获取输出
def execute_command(command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()  # 等待命令执行完成
    output = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")
    return output, error, exit_status

    # 执行第一条命令
output, error, status = execute_command("mkdir service")
print(output)
if error:
    print(f"Error: {error}")
    # 等待命令执行完成
time.sleep(2)

    # 执行第二条命令
output, error, status = execute_command("chmod 777 service")
print(output)
if error:
    print(f"Error: {error}")
time.sleep(2)

    # 执行第二条命令
output, error, status = execute_command("cd ../")
print(output)
if error:
    print(f"Error: {error}")
time.sleep(2)

# 本地处理通过subprocess.Popen
local_command = f"scp -i {key_file_path} {path_to_file} ec2-user@{hostname}:/home/ec2-user"
process = subprocess.Popen(local_command, shell=True)
process.wait()

local_command2= f"scp -i {key_file_path} {path_to_decompress} ec2-user@{hostname}:/home/ec2-user"
process = subprocess.Popen(local_command2, shell=True)
process.wait()

output, error, status = execute_command("python decompress_service.py")
print(output)
if error:
    print(f"Error: {error}")
    # 等待命令执行完成
time.sleep(2)
ssh_client.close()