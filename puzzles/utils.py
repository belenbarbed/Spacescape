import time

DELAY = 0.1

def printOut(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(DELAY)
    print()
