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
from utils import printOut, clearScreen
sys.path.pop(0)


# assuming 6 resistors
NUM_RESISTORS = 6

resistors = ['130', '8000', '200', '2400', '4000', '120']

ser = None

def signal_handler(sig, frame):
    global ser
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def resistorPuzzle(debug=False):
    clearScreen()

    global ser

    # for raspberry pi (as found from ls /dev/tty/ACM*)
    ser = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=0.1)
    # for MAC only:
    #ser = serial.Serial("/dev/tty.usbmodemFB0001", baudrate=9600, timeout=0.1)

    # need sleep here to set up serial (mac = 2, pi = 0.6)
    ser.write(b'reset\n')
    read_ser = ser.readline()
    while read_ser != b'reset\r\n':
        ser.write(b'reset\n')
        read_ser = ser.readline()

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

    attempt = ''
    while attempt != code1 and attempt != code2:
        attempt = input('Enter one repair code: ')
    remaining = code2 if attempt == code1 else code1
    attempt = ''
    while attempt != remaining:
        attempt = input('Enter another repair code: ')

    print('Repair code accepted, pod systems now repairing', end='')
    for i in range(5):
        print('.', end='', flush=True)
        time.sleep(0.5)
    print('Complete!')

    printOut('Engine Status:\tOK\nHyperdrive:\tONLINE\nLife Support:\tLIMITED - ? mins remaining')

    ser.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The resistor puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
        dest='debug', help='enable debug mode')
    args = parser.parse_args()

    resistorPuzzle(debug=args.debug)
