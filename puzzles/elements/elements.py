from mendeleev import element
import random
import re
import argparse

parser = argparse.ArgumentParser(description='The periodic table puzzle.')
parser.add_argument('-d', '--debug', default=False, action='store_true', dest='debug', help='enable debug mode')
args = parser.parse_args()

with open('words.txt', 'r') as f:
    words = [line.strip() for line in f]
# print(words)
# print(len(words))

# word to use for code
word = words[random.randint(0, len(words))]
# print(word)
print('-- ACCESS POD MAINFRAME --\nUser: ' + word.upper())

elements = re.findall(r'([A-Z][a-z]*)', word)
# print(elements)

code = ''
for item in elements:
    code += str(element(item).atomic_number)

if args.debug: print(code)

attempt = ''
while attempt != code:
    attempt = input('Password: ')

print('Sign-in successful!')