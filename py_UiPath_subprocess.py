import os, time
import subprocess
import pyautogui

command  = r"C:\Users\terafast\Documents\UiPath\Desktop_automation\anydeskautomation.xaml"
subprocess.Popen(command, shell=True)
print("\n UIPath Opening process...!!!")
time.sleep(30)

print("\n F6 KEY PRESSED...")
pyautogui.press('f6')





