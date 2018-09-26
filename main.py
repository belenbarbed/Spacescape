#!/usr/bin/python3

import argparse
import curses
import time
import signal, sys
from subprocess import call
import os

# puzzles
from puzzles.asteroids.asteroids import asteroidPuzzle
from puzzles.elements.elements import elementPuzzle
from puzzles.resistors.resistors import resistorPuzzle

from common import printOut, clearScreen, disableButton, disableKeys
from utils.door.door import openDoor
from utils.lights.lights import lights

start = 'videos/start2.mp4'
static = 'videos/static.mp4'
journey = 'videos/journey.mp4'
asteroids = 'videos/asteroids.mp4'
landing = 'videos/landing1.mp4'

# ^C handler
def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# main function
def main(debug=False, gametime=10.0):
    if not debug:
        disableButton()
        os.system("./utils/numlock.sh")
    
    clearScreen()
    
    # user settles down and presses numpad 'enter' to start
    input('PRESS ENTER TO LAUNCH')
    if not debug:
        disableKeys()
    time.sleep(1)

    # close door electromagnets
    openDoor(False)
    
    clearScreen()
    printOut('--- WELCOME ON BOARD ---')
    printOut('POD NOW LAUNCHING...')
    time.sleep(2)
    clearScreen()
    lights('dim')

    if not debug:
        # open video of launch and crash (blocking)
        os.system("omxplayer --no-keys --no-osd -o local " + start + " --win '0 0 1080 960' > /dev/null &")
        time.sleep(28)
        lights('flash')
        lights('dim')
        time.sleep(2)

    lights('fade')
    
    # open video of static space (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + static + " --win '0 0 1080 960' > /dev/null &")

    printOut('SYSTEMS DAMAGED DUE TO ASTEROID COLLISION')
    time.sleep(2)
    printOut('\nSYSTEMS REBOOTING')
    for i in range(0, 5):
        print('.', end='', flush=True)
        time.sleep(1)

    # start countdown
    timeout = time.time() + (gametime * 60)
    m, s = divmod(timeout-time.time(), 60)
    printOut('\n\n--- WARNING ---\nLIFE SUPPORT DAMAGED: {:.0f} MINUTES {} SECONDS REMAINING'.format(m, int(s)))
    printOut('PLEASE FOLLOW INSTRUCTIONS TO ENSURE SURVIVAL')
    time.sleep(2)

    # open video of traversing space (in parallel)
    os.system("killall -s SIGINT omxplayer.bin")
    os.system("omxplayer --no-keys --no-osd -o local " + journey + " --win '0 0 1080 960' > /dev/null &")
    
    # 1st PUZZLE: login (elements.py)
    elementPuzzle(timeout, debug)
    time.sleep(2)

    # open video of asteroids approaching (in parallel)
    os.system("killall -s SIGINT omxplayer.bin")
    os.system("omxplayer --no-keys --no-osd -o local " + asteroids + " --win '0 0 1080 960' > /dev/null &")

    # 2nd PUZZLE: asteroid avoiding minigame (asteroids.py)
    deaths = asteroidPuzzle(timeout, debug)

    # open video of static space (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + static + " --win '0 0 1080 960' > /dev/null &")

    # discount time depending on no. of deaths
    if deaths >= 1:
        timeout -= 10
        if deaths >= 2:
            timeout -= deaths * 5
        printOut('\n\n --- WARNING ---\nLIFE SUPPORT DAMAGED BY ASTEROID COLLISION')
        m, s = divmod(timeout-time.time(), 60)
        printOut('{:.0f} MINUTE{} {} SECONDS REMAINING'.format(m, 'S' if m >= 2.0 else '', int(s)))
    time.sleep(2)

    # 3rd PUZZLE: repair codes (resistors.py)
    resistorPuzzle(timeout, debug)
    os.system("killall -s SIGINT omxplayer.bin")
    os.system("omxplayer --no-keys --no-osd -o local " + journey + " --win '0 0 1080 960' > /dev/null &")
    time.sleep(2)

    lights('dim')
    # open video of landing (in parallel)
    os.system("killall -s SIGINT omxplayer.bin")
    os.system("omxplayer --no-keys --no-osd -o local " + landing + " --win '0 0 1080 960' > /dev/null &")

    # stop countdown
    final_time = timeout - time.time()

    # tell user they passed!
    clearScreen()
    printOut('POD SAFELY LANDED')
    lights('fade')

    # user presses numpad 'enter' to open bay door
    if not debug:
        disableKeys(False)
    printOut('\n\nTHANKS FOR PLAYING!\n\n')
    m, s = divmod(final_time, 60)
    printOut('{}YOU FINISHED WITH {:.0f} MINUTE{} {} SECONDS {}.'.format('CONGRATULATIONS! ' if final_time >= 0 else '', m, 'S' if m >= 2.0 else '', int(s), 'REMAINING' if final_time >= 0 else 'OVERTIME'))
    printOut('\n\n--- PRESS ENTER TO OPEN POD DOOR ---')
    input('')

    # open door electromagnets
    openDoor(True)

    # Wait for user to leave
    time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Master script for puzzles and screen mgmt')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    parser.add_argument('-t', '--time', default=10.0, type=int, dest='time', help='set game time')
    args = parser.parse_args()

    while True:
        main(debug=args.debug, gametime=args.time)
