import time
import os

DELAY = 0.1

def printOut(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(DELAY)
    print()

def clearScreen():
    os.system('clear')
