import argparse
import time
import signal, sys

# puzzles
from puzzles.asteroids.asteroids import asteroidPuzzle
from puzzles.elements.elements import elementPuzzle
from puzzles.resistors.resistors import resistorPuzzle

from utils import printOut, clearScreen, disableButton, disableKeys

TIME = 5 # Game time in minutes

# ^C handler
def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# main function
def main(debug=False):
    clearScreen()
    if not debug:
        disableButton()

    # TODO: open video of space in top of screen

    # user settles down and presses numpad 'enter' to start
    input('PRESS ENTER TO LAUNCH')
    if not debug:
        disableKeys()
    time.sleep(1)
    clearScreen()
    printOut('--- WELCOME ON BOARD ---')
    printOut('POD NOW LAUNCHING...')
    time.sleep(2)
    clearScreen()

    # TODO: open video of escape and crash
    printOut('SYSTEMS DAMAGED DUE TO ASTEROID COLLISION')

    # TODO: start countdown
    timeout = time.time() + (TIME * 60)
    m, s = divmod(timeout-time.time(), 60)
    printOut('LIFE SUPPORT DAMAGED: {:.0f} MINUTES {:.0f} SECONDS REMAINING'.format(m, s))
    printOut('PLEASE FOLLOW INSTRUCTIONS TO ENSURE SURVIVAL')
    time.sleep(2)

    # TODO: open video of traversing space

    # 1st PUZZLE: login (elements.py)
    elementPuzzle(timeout, debug)
    time.sleep(2)

    # puzzle returns = puzzle passed

    # TODO: open video of asteroids approaching
    
    # TODO: turn off main monitor

    # 2nd PUZZLE: asteroid avoiding minigame (asteroids.py)
    deaths = asteroidPuzzle(timeout, debug)

    # puzzle returns = puzzle passed

    # TODO: discount time depending on no. of deaths
    if deaths >= 1:
        timeout -= 10
        if deaths >= 2:
            timeout -= deaths * 5
        printOut('LIFE SUPPORT DAMAGED BY ASTEROID COLLISION')
        m, s = divmod(timeout-time.time(), 60)
        printOut('{:.0f} MINUTES {:.0f} SECONDS REMAINING'.format(m, s)) 
    time.sleep(2)

    # TODO: open video of traversing space

    # 3rd PUZZLE: repair codes (resistors.py)
    resistorPuzzle(timeout, debug)
    time.sleep(2)

    # puzzle returns = puzzle passed

    # TODO: open video of landing

    # TODO: stop countdown
    final_time = timeout - time.time()

    # TODO: tell user they passed!
    clearScreen()
    printOut('POD SAFELY LANDED')
    m, s = divmod(final_time, 60)
    printOut('{:.0f} MINUTES {:.0f} SECONDS OF LIFE SUPPORT REMAINING'.format(m, s))

    # user presses numpad 'enter' to open bay door
    if not debug:
        disableKeys(False)
    printOut('--- PRESS ENTER TO OPEN POD DOOR ---')
    input('')

    # TODO: open door electromagnets

    # TODO: reset all puzzles + timer display

    # Wait for user to leave
    time.sleep(5)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Master script for puzzles and screen mgmt')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    main(debug=args.debug)
