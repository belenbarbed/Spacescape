import argparse

from asteroids import asteroids
from elements import elements
from resistors import resistors
from utils import printOut, clearScreen

# main function
def main(debug=False):
    clearScreen()

    # TODO: reset all puzzles (?)

    # TODO: open video of space in top of screen

    # TODO: user settles down and presses numpad 'enter' to start
    input('Press enter to start')

    # TODO: open video of escape and crash
    if debug:
        print('')

    # TODO: start countdown

    # TODO: open video of traversing space

    # TODO: 1st PUZZLE: login (elements.py)

    # puzzle returns = puzzle passed

    # TODO: 2nd PUZZLE: repair codes (resistors.py)

    # puzzle returns = puzzle passed

    # TODO: open video of asteroids approaching

    # TODO: 3rd PUZZLE: asteroid avoiding minigame (asteroids.py)

    # puzzle returns = puzzle passed

    # TODO: discount time depending on no. of deaths

    # TODO: open video of traversing space (or landing??)

    # TODO: stop countdown

    # TODO: tell user they passed!

    # TODO: user presses numpad 'enter' to open bay door

    # TODO: open door electromagnets

    # TODO: reset all puzzles (?)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Master script for puzzles and screen mgmt')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    main(debug=args.debug)
