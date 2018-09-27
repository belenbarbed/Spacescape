import argparse
import random
import serial
import struct
import time
import signal, sys

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from common import printOut, clearScreen, disableKeys
sys.path.pop(0)


# assuming 6 resistors
NUM_RESISTORS = 6

resistors = ['33000', '5100', '4400', '470', '8000', '85000']

ser = None

def signal_handler(sig, frame):
    global ser
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


HINTS = {
            1: "THERE IS A CLUE TO THE RIGHT, BELOW THE DESK.",
            2: "THERE IS A PANEL TO YOUR BACK LEFT, THE PUZZLE CAN BE FOUND INSIDE.",
            3: "THE REPAIR CODES ARE RELATED TO THE RESISTORS WITH RED WARNING LIGHTS.",
            4: "CONVERT THE RESISTOR INTO ITS RESISTANCE USING THE RESISTOR COLOUR CHART.\nDO THIS FOR BOTH RESISTORS TO GET THE TWO REPAIR CODES."
        }

def hint(counter):
    accept = input('YOU HAVE REQUESTED A HINT, ARE YOU SURE?\nPRESS * AND ENTER TO ACCEPT\nPRESS ENTER TO REJECT\n')
    if accept == '*':
        if counter < 4:
            counter += 1
        print(HINTS[counter])
    return counter


def resistorPuzzle(gametime, debug=False):
    clearScreen()
    hint_count = 0

    if not debug:
        disableKeys()

    global ser
    
    if not tryConnect('/dev/ttyUSB1', b'RESISTORS\r\n'):
        if not tryConnect('/dev/ttyUSB0', b'RESISTORS\r\n'):
            try:
                if not tryConnect('/dev/ttyACM1', b'RESISTORS\r\n'):
                    return
            except:
                if not tryConnect('/dev/ttyACM0', b'RESISTORS\r\n'):
                    return

    # pick 2 random resistors
    resistor1 = random.randint(0,NUM_RESISTORS-1)
    resistor2 = random.randint(0,NUM_RESISTORS-1)
    while resistor2 == resistor1:
        # ensure resistor 2 is not same as resistor 1
        resistor2 = random.randint(0,NUM_RESISTORS-1)

    if debug:
        print('Resistor 1: {}\nResistor 2: {}'.format(resistor1, resistor2))

    code1 = resistors[resistor1]
    code2 = resistors[resistor2]

    if debug:
        print('Code 1: {}'.format(code1))
        print('Code 2: {}'.format(code2))

    ser.write((str(resistor1)+'\n').encode())
    ser.write((str(resistor2)+'\n').encode())

    if debug:
        print('Values sent')

    while True:
        read_ser=ser.readline()
        if read_ser == b'ready\r\n':
            if debug:
                print('Arduino ready, LEDs lit')
            break

    printOut('--- WARNING ---')
    printOut('ENGINE DAMAGED DUE TO ASTEROID COLLISION')
    printOut('ATTEMPTING AUTOMATIC REPAIR')
    for i in range(5):
        print('.', end='', flush=True)
        time.sleep(0.5)
    printOut(' AUTOMATIC REPAIR FAILED!')
    printOut('MANUAL OVERRIDE REQUIRED\n\n')

    # Enable numpad
    if not debug:
        disableKeys(False)

    attempt = '0'
    while int(attempt) != int(code1) and int(attempt) != int(code2):
        attempt = input('ENTER ENGINE REPAIR CODE 1/2: ')
        if attempt == '*':
            hint_count = hint(hint_count)
        try:
            int(attempt)
        except ValueError:
            attempt = '0'
    remaining = code2 if int(attempt) == int(code1) else code1
    if int(attempt) == int(code1):
        ser.write((str(resistor1)+'ok\n').encode())
    else:
        ser.write((str(resistor2)+'ok\n').encode())
    
    printOut('\n')

    attempt = '0'
    while int(attempt) != int(remaining):
        attempt = input('ENTER ENGINE REPAIR CODE 2/2: ')
        if attempt == '*':
            hint_count = hint(hint_count)
        try:
            int(attempt)
        except ValueError:
            attempt = '0'
    if int(attempt) == int(code1):
        ser.write((str(resistor1)+'ok\n').encode())
    else:
        ser.write((str(resistor2)+'ok\n').encode())

    # Disable numpad
    if not debug:
        disableKeys()
    clearScreen()

    printOut('REPAIR CODES ACCEPTED, ENGINE NOW REPAIRING')
    for i in range(5):
        print('.', end='', flush=True)
        time.sleep(0.5)
    printOut(' COMPLETE!')

    printOut('\n\n--- POD STATUS ---')
    m, s = divmod(gametime-time.time(), 60)
    printOut('ENGINE STATUS:\tOK\nHYPERDRIVE:\tONLINE\nLIFE SUPPORT:\tLIMITED - {:.0f} MINUTE{} {} SECONDS REMAINING\nHINTS USED:\t{}'.format(m, 'S' if m >= 2.0 else '', int(s), hint_count))

    ser.close()

    return hint_count

def tryConnect(board, word):
    global ser

    ser = serial.Serial(board, baudrate=9600, timeout=0.1)
    ser.write(b'reset\n')
    read_ser = ser.readline()
    while read_ser != b'reset\r\n':
        ser.write(b'reset\n')
        read_ser = ser.readline()

    # Arduino connected, is it right one?
    if ser.readline() == word:
        return True

    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The resistor puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
        dest='debug', help='enable debug mode')
    args = parser.parse_args()

    resistorPuzzle(gametime=time.time()+300, debug=args.debug)
