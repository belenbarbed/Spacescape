import serial
import signal, sys
import argparse

ser = None

def signal_handler(sig, frame):
    global ser
    ser.close()
    sys.exit(0)

# openDoor(true) opens
# openDoor(false) closes
def openDoor(open=True, debug=False):
    global ser

    # connect to Arduino
    if not tryConnect('/dev/ttyUSB1', b'RELAY\r\n'):
        if not tryConnect('/dev/ttyUSB0', b'RELAY\r\n'):
            try:
                if not tryConnect('/dev/ttyACM1', b'RELAY\r\n'):
                    return
            except:
                if not tryConnect('/dev/ttyACM0', b'RELAY\r\n'):
                    return

    ser.write(b'openDoor\n') if open else ser.write(b'closeDoor\n')

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
    parser = argparse.ArgumentParser(description='Door opening/closing code.')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
        dest='debug', help='enable debug mode')
    args = parser.parse_args()

    openDoor(True, debug=args.debug)
    time.sleep(5)
    openDoor(False, debug=args.debug)
