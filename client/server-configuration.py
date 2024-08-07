import pyautogui
import os
import time
import subprocess
import ctypes
import pyperclip

#ctypes.windll.User32.PostMessageW(None, 274, 65535, 0)

subprocess.Popen('cd '+os.path.dirname(__file__), shell=True)
 
# 执行第二条命令
ii=input('please type in the server information(for instance ec2-54-175-40-110.compute-1.amazonaws.com):')

subprocess.Popen('ssh -o UserKnownHostsFile=NUL -i '+os.path.dirname(__file__)+"/key.pem"+' ec2-user@'+ii)

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

cmd_exec_ori("yes",5)
cmd_exec_ori("cd service",5)
cmd_exec_ori("sh 1.sh")

time_original=time.time()

switch=True

subprocess.Popen('cmd',creationflags=subprocess.CREATE_NEW_CONSOLE)

time.sleep(1)

pyautogui.click()

cmd_exec('ssh -o UserKnownHostsFile=NUL -N -L 5000:localhost:5000 -i '+os.path.dirname(__file__)+"\\key.pem"+" ec2-user"+"@"+ii)
cmd_exec('yes')

while True:
    '''time_now=time.time()-time_original
    if time_now-time_original>30:
        if switch==True:
            subprocess.Popen('cmd', creationflags=subprocess.CREATE_NEW_CONSOLE)
    '''
    pass