from mendeleev import element
import random
import re
import argparse

def elementPuzzle(debug=False):
    with open('words.txt', 'r') as f:
        words = [line.strip() for line in f]

    # word to use for code
    word = words[random.randint(0, len(words))]
    print('-- ACCESS POD MAINFRAME --\nUser: ' + word.upper())

    elements = re.findall(r'([A-Z][a-z]*)', word)

    code = ''
    for item in elements:
        code += str(element(item).atomic_number)

    if debug: print(code)

    attempt = ''
    while attempt != code:
        attempt = input('Password: ')

    print('Sign-in successful!')

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The periodic table puzzle.')
    parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug', help='enable debug mode')
    args = parser.parse_args()

    elementPuzzle(debug=args.debug)