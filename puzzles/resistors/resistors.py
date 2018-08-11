import argparse
import random
import serial
import struct
import time
import signal, sys

# assuming 6 resistors
NUM_RESISTORS = 6

resistors = ['130', '8000', '200', '2400', '4000', '120']

ser = None

def signal_handler(sig, frame):
    print('handling! quit')
    global ser
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def resistorPuzzle(debug=False):
    # change ACM number as found from ls /dev/tty/ACM*
    global ser
    ser = serial.Serial("/dev/ttyACM0", 9600)
    # for MAC only:
    # ser = serial.Serial("/dev/tty.usbmodemFB0001", 9600)
    time.sleep(0.6)
    ser.baudrate = 9600
    
    sleep = 1
    
    # pick 2 random resistors
    resistor1 = random.randint(0,NUM_RESISTORS-1)
    resistor2 = random.randint(0,NUM_RESISTORS-1)
    while resistor2 == resistor1:
        # ensure resistor 2 is not same as resistor 1
        resistor2 = random.randint(0,NUM_RESISTORS-1)

    if debug:
        print('Resistor 1: {}\nResistor 2: {}'.format(resistor1, resistor2))

    code = resistors[resistor1] + resistors[resistor2]

    if debug:
        print('Code: {}'.format(code))
    #ser.write_timeout = 0.01
    
    for i in range(0,10):
        ser.write(b'banter\n')
    
    ser.write(b'reset\n1\n2\n')
    
    ser.write((str(resistor1)+'\n').encode())
    #time.sleep(sleep)
    ser.write((str(resistor2)+'\n').encode())
    #time.sleep(sleep)
    #ser.write(b'reset\n3\n5\n')
    if debug:
        print('Values sent')

    while True:
        read_ser=ser.readline()
        if read_ser == b'ready\r\n':
            if debug:
                print('Arduino ready, LEDs lit')
            break

    attempt = ''
    while attempt != code:
        attempt = input('Enter repair code: ')
    
    print('Repair code accepted, pod systems now repairing', end='')
    for i in range(5):
        print('.', end='', flush=True)
        time.sleep(0.5)
    print('Complete!')

    message = 'Engine Status:\tOK\nHyperdrive:\tONLINE\nLife Support:\tLIMITED - ? mins remaining\n'
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The resistor puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug', help='enable debug mode')
    args = parser.parse_args()

    resistorPuzzle(debug=args.debug)
