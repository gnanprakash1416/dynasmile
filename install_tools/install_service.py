import pyautogui
import os
import time
import subprocess
import ctypes
import pyperclip

#ctypes.windll.User32.PostMessageW(None, 274, 65535, 0)

subprocess.Popen('cd '+os.path.dirname(os.path.dirname(__file__))+"/client", shell=True)

path_to_mem_key=os.path.dirname(os.path.dirname(__file__))+"\client"+"\key.pem"
# 执行第二条命令
ii=input('please type in the server information(for instance ec2-54-175-40-110.compute-1.amazonaws.com):')

subprocess.Popen('ssh -o UserKnownHostsFile=NUL -i '+path_to_mem_key+' ec2-user@'+ii)

time.sleep(10)

#pyautogui.press("shift")

def cmd_exec_ori(command,timee=5):
    pyautogui.write(command)
    pyautogui.press("enter")
    time.sleep(timee)

def cmd_exec(command,timee=5):
    pyperclip.copy(command)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')
    pyautogui.press("enter")
    time.sleep(timee)

cmd_exec_ori("mkdir service",5)
cmd_exec_ori("chmod 777 service",5)

time_original=time.time()

switch=True

subprocess.Popen('cmd',creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(1)

pyautogui.click()

path_to_file=os.path.dirname(os.path.dirname(__file__))+"/server/service.zip"

path_to_decompress=os.path.dirname(os.path.dirname(__file__))+"/server/decompress_service.py"

cmd_exec('scp -i '+path_to_mem_key+' '+path_to_file+" ec2-user"+"@"+ii+':/home/ec2-user')

subprocess.Popen('cmd',creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(1)

pyautogui.click()

cmd_exec('scp -i '+path_to_mem_key+' '+path_to_decompress+" ec2-user"+"@"+ii+':/home/ec2-user')

while True:
    '''time_now=time.time()-time_original
    if time_now-time_original>30:
        if switch==True:
            subprocess.Popen('cmd', creationflags=subprocess.CREATE_NEW_CONSOLE)
    '''
    pass