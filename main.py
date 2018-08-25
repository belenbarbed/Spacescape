import argparse
import time
import signal, sys

# puzzles
from puzzles.asteroids.asteroids import asteroidPuzzle
from puzzles.elements.elements import elementPuzzle
from puzzles.resistors.resistors import resistorPuzzle

from utils import printOut, clearScreen

# ^C handler
def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# main function
def main(debug=False):
    clearScreen()

    # TODO: open video of space in top of screen

    # user settles down and presses numpad 'enter' to start
    input('Press enter to start')
    time.sleep(1)
    clearScreen()
    printOut('--- WELCOME ON BOARD! ---')

    # TODO: open video of escape and crash

    # TODO: start countdown

    # TODO: open video of traversing space

    # 1st PUZZLE: login (elements.py)
    elementPuzzle(debug)

    # puzzle returns = puzzle passed

    # TODO: open video of asteroids approaching

    # 2nd PUZZLE: asteroid avoiding minigame (asteroids.py)
    asteroidPuzzle(debug)

    # puzzle returns = puzzle passed

    # TODO: discount time depending on no. of deaths

    # TODO: open video of traversing space

    # 3rd PUZZLE: repair codes (resistors.py)
    resistorPuzzle(debug)

    # puzzle returns = puzzle passed

    # TODO: open video of landing

    # TODO: stop countdown

    # TODO: tell user they passed!

    # user presses numpad 'enter' to open bay door
    clearScreen()
    printOut('--- PRESS ENTER TO OPEN BAY DOORS ---')
    input('')

    # TODO: open door electromagnets

    # TODO: reset all puzzles + timer display

    # Wait for user to leave
    time.sleep(30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Master script for puzzles and screen mgmt')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    main(debug=args.debug)
