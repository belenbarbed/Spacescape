from random import randint
import curses
import time
import sys, signal
import pygame

from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from utils import printOut, clearScreen
sys.path.pop(0)


HEIGHT = 20
WIDTH = 80
TIMEOUT = 35
SPEED = 1.0
RATE = 0.60


def sig_handler(sig, frame):
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

class Player():
    def __init__(self):
        self.x = int(WIDTH/2)
        self.y = HEIGHT-2
        self._icon = '^'
        self._deaths = 0
        self.last_death = 0

    def left(self):
        if self.x > 1 and self._icon != '*':
            self.x -= 1

    def right(self):
        if self.x < WIDTH-2 and self._icon != '*':
            self.x += 1

    def getIcon(self):
        return self._icon

    def setIcon(self, newIcon='^'):
        self._icon = newIcon

    def die(self):
        self._deaths += 1
        self.last_death = time.time()

    def deaths(self):
        return self._deaths

class Asteroid():
    def __init__(self):
        self.x = randint(1, WIDTH-2)
        self.y = 0
        self.exist = True

    def fall(self):
        if self.y < HEIGHT-1:
            self.y += 1
        else:
            self.exist = False


def hit(player, asteroid, sound=None):
    # FIXME: player disappears when hitting asteroid sideways
    if player.x == asteroid.x and player.y == asteroid.y:
        if sound:
            pygame.mixer.Sound.play(sound)
        asteroid.exist = False
        if player.getIcon() == '^':
            player.die()
        return True
    return False


def asteroids():
    pygame.mixer.init()
    pygame.init() #turn all of pygame on.
    hit_sound = pygame.mixer.Sound('hit.wav')

    clearScreen()

    printOut('--- WARNING! ---\nESCAPE POD NOW ENTERING HIGHLY DENSE ASTEROID FIELD')
    printOut('MANUAL NAVIGATION REQUIRED')
    printOut('ENTERING FIELD IN')
    for i in [3, 2, 1]:
        print(i)
        time.sleep(1)

    pygame.mixer.music.load('moon.wav')
    pygame.mixer.music.play(-1)
    
    timeout = time.time() + TIMEOUT
    speed = SPEED
    curses.initscr()
    win = curses.newwin(HEIGHT, WIDTH, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    player = Player()
    win.addch(player.y, player.x, player.getIcon())

    key = None
    
    asteroids = []

    interval = time.time()
    curr_time = time.time()
    
    while True:
        if time.time() > timeout:
            break
        if time.time() > curr_time + 5:
            speed *= RATE
            curr_time = time.time()
        win.border(0)
        win.addstr(0, 0, 'Time Left : {:.2f} '.format(timeout-time.time()))
        win.addstr(HEIGHT-1, WIDTH-13, 'Speed : {:.2f}'.format(speed))
        win.addstr(HEIGHT-1, 1, 'Deaths : {} '.format(player.deaths()))

        event = win.getch()
        key = None if event == -1 else event
        

        if key == ord('a'):
            player.left()
            win.addch(player.y, player.x, player.getIcon())
            win.addch(player.y, player.x+1, ' ')
        if key == ord('d'):
            player.right()
            win.addch(player.y, player.x, player.getIcon())
            win.addch(player.y, player.x-1, ' ')

        if time.time() > player.last_death + 1:
            player.setIcon()

        if time.time() > interval + speed:
            win.addch(player.y, player.x, player.getIcon())
            aster = Asteroid()
            asteroids.append(aster)
            for asteroid in asteroids:
                asteroid.fall()
                if asteroid.exist:
                    if hit(player, asteroid, hit_sound):
                        player.setIcon('*')
                        win.addch(player.y, player.x, player.getIcon())
                        win.addch(asteroid.y-1, asteroid.x, ' ')
                    else:
                        win.addch(asteroid.y, asteroid.x, '@')
                        win.addch(asteroid.y-1, asteroid.x, ' ')
            interval = time.time()

    curses.endwin()
    pygame.mixer.music.fadeout(2000)

    clearScreen()
    printOut('NAVIGATION THROUGH ASTEROID FIELD COMPLETE...')
    printOut('POD WAS HIT {} TIME{}'.format(player.deaths(), '' if player.deaths()==1 else 'S'))

if __name__ == '__main__':
    asteroids()
