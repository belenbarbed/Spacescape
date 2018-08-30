from mendeleev import element
import random
import re
import time
import argparse

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from utils import printOut, clearScreen, disableKeys
sys.path.pop(0)


def elementPuzzle(gametime, debug=False):
    clearScreen()

    with open('puzzles/elements/words.txt', 'r') as f:
        words = [line.strip() for line in f]

    # word to use for code
    word = words[random.randint(0, len(words)-1)]
    printOut('--- ACCESS POD MAINFRAME ---')
    #print('User: ' + word.upper())
    print('User: ' + word)

    elements = re.findall(r'([A-Z][a-z]*)', word)

    code = ''
    for item in elements:
        code += str(element(item).atomic_number)

    if debug: print(code)

    # Enable numpad
    if not debug:
        disableKeys(False)

    attempt = ''
    while attempt != code:
        attempt = input('Password: ')

    # Disable numpad
    if not debug:
        disableKeys()

    printOut('ACCESS GRANTED')
    printOut('--- POD STATUS ---')
    m, s = divmod(gametime-time.time(), 60)
    printOut('ENGINE STATUS:\tOK\nHYPERDRIVE:\tOFFLINE\nLIFE SUPPORT:\tLIMITED - {:.0f} MINUTES {} SECONDS REMAINING'.format(m, int(s)))

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The periodic table puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    elementPuzzle(gametime=time.time()+300, debug=args.debug)
