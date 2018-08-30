import time
import os
import subprocess

DELAY = 0.05
DEVICE_ID = '8'

def printOut(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(DELAY)
    print()

def clearScreen():
    os.system('clear')

def disableButton(true=True):
    if true:
        subprocess.call(['sudo', 'systemctl', 'stop', 'gpioneer'])
    else:
        subprocess.call(['sudo', 'systemctl', 'start', 'gpioneer'])

def disableKeys(true=True):
    if true:
        subprocess.call(['xinput', 'disable', DEVICE_ID])
    else:
        subprocess.call(['xinput', 'enable', DEVICE_ID])
