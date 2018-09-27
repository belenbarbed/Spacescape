from mendeleev import element
import random
import re
import time
import argparse

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from common import printOut, clearScreen, disableKeys
sys.path.pop(0)

HINTS = {
            1: "TAKE A LOOK AROUND THE POD, CLUES MAY BE HIDDEN.",
            2: "THERE IS A PANEL TO YOUR BACK LEFT, A CLUE CAN BE FOUND ON THE PANEL DOOR.",
            3: "THE USER'S PASSWORD IS RELATED TO THE PERIODIC TABLE.",
            4: "TRANSLATE THE USER'S NAME INTO CHEMICAL ELEMENT NUMBERS VIA THE PERIODIC\nTABLE. THE SEQUENCE OF NUMBERS FORM THE PASSWORD YOU NEED."
        }

def hint(counter):
    accept = input('YOU HAVE REQUESTED A HINT, ARE YOU SURE?\nPRESS * AND ENTER TO ACCEPT\nPRESS ENTER TO REJECT\n')
    if accept == '*':
        if counter < 4:
            counter += 1
        print(HINTS[counter])
    return counter

def elementPuzzle(gametime, debug=False):
    clearScreen()
    hint_count = 0

    with open('puzzles/elements/words.txt', 'r') as f:
        words = [line.strip() for line in f]

    # word to use for code
    word = words[random.randint(0, len(words)-1)]
    printOut('--- ACCESS POD MAINFRAME ---')
    
    elements = re.findall(r'([A-Z][a-z]*)', word)

    code = ''
    for item in elements:
        code += str(element(item).atomic_number)

    if debug: print(code)

    # Enable numpad
    if not debug:
        disableKeys(False)

    attempt = '0'
    while int(attempt) != int(code):
        #print('User: ' + word.upper())
        print('\nUser: ' + word)
        attempt = input('Password: ')
        if attempt == '*':
            hint_count = hint(hint_count)
        try:
            int(attempt)
        except ValueError:
            attempt = '0'

    # Disable numpad
    if not debug:
        disableKeys()

    printOut('ACCESS GRANTED')
    printOut('\n\n--- POD STATUS ---')
    m, s = divmod(gametime-time.time(), 60)
    printOut('ENGINE STATUS:\tOK\nHYPERDRIVE:\tOFFLINE\nLIFE SUPPORT:\tLIMITED - {:.0f} MINUTES {} SECONDS REMAINING\nHINTS USED:\t{}'.format(m, int(s), hint_count))

    return hint_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The periodic table puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug',
        help='enable debug mode')
    args = parser.parse_args()

    elementPuzzle(gametime=time.time()+300, debug=args.debug)
