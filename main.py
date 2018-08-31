#!/usr/bin/python3

import argparse
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

TIME = 5 # Game time in minutes

start = 'videos/start1.mp4'
static = 'videos/static.mp4'
journey = 'videos/journey.mp4'
asteroids = 'videos/asteroids_short.mp4'
landing = 'videos/landing.mp4'

# ^C handler
def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# main function
def main(debug=False):
    clearScreen()
    if not debug:
        disableButton()
        os.system("./utils/numlock.sh")

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

    # open video of launch and crash (blocking)
    os.system("omxplayer --no-osd " + start + " --win '0 0 1080 960' > /dev/null")
    printOut('SYSTEMS DAMAGED DUE TO ASTEROID COLLISION')
    
    # open video of static space (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + static + " --win '0 0 1080 960' > /dev/null &")

    # start countdown
    timeout = time.time() + (TIME * 60)
    m, s = divmod(timeout-time.time(), 60)
    printOut('LIFE SUPPORT DAMAGED: {:.0f} MINUTES {} SECONDS REMAINING'.format(m, int(s)))
    printOut('PLEASE FOLLOW INSTRUCTIONS TO ENSURE SURVIVAL')
    time.sleep(2)

    # open video of traversing space (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + journey + " --win '0 0 1080 960' > /dev/null &")
    
    # 1st PUZZLE: login (elements.py)
    elementPuzzle(timeout, debug)
    time.sleep(2)

    # open video of asteroids approaching (in parallel)
    os.system("omxplayer --no-osd " + asteroids + " --win '0 0 1080 960' > /dev/null &")

    # 2nd PUZZLE: asteroid avoiding minigame (asteroids.py)
    deaths = asteroidPuzzle(timeout, debug)

    # discount time depending on no. of deaths
    if deaths >= 1:
        timeout -= 10
        if deaths >= 2:
            timeout -= deaths * 5
        printOut('LIFE SUPPORT DAMAGED BY ASTEROID COLLISION')
        m, s = divmod(timeout-time.time(), 60)
        printOut('{:.0f} MINUTES {} SECONDS REMAINING'.format(m, int(s)))
    time.sleep(2)

    # open video of traversing space (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + journey + " --win '0 0 1080 960' > /dev/null &")

    # 3rd PUZZLE: repair codes (resistors.py)
    resistorPuzzle(timeout, debug)
    time.sleep(2)

    # open video of landing (in parallel)
    os.system("omxplayer --no-keys --no-osd -o local " + landing + " --win '0 0 1080 960' > /dev/null &")

    # stop countdown
    final_time = timeout - time.time()

    # tell user they passed!
    clearScreen()
    printOut('POD SAFELY LANDED')
    m, s = divmod(final_time, 60)
    printOut('{:.0f} MINUTES {} SECONDS OF LIFE SUPPORT REMAINING'.format(m, int(s)))

    # user presses numpad 'enter' to open bay door
    if not debug:
        disableKeys(False)
    printOut('--- PRESS ENTER TO OPEN POD DOOR ---')
    input('')

    # open door electromagnets
    openDoor(True)

    # Wait for user to leave
    time.sleep(5)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Master script for puzzles and screen mgmt')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    main(debug=args.debug)
