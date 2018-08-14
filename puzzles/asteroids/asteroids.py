from random import randint
import curses
import time
import sys, signal

HEIGHT = 10
WIDTH = 40
TIMEOUT = 30

def sig_handler(sig, frame):
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

class Player():
    def __init__(self):
        self.x = int(WIDTH/2)
        self.y = HEIGHT-2

    def left(self):
        if self.x > 1:
            self.x -= 1

    def right(self):
        if self.x < WIDTH-2:
            self.x += 1

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


def hit(player, asteroid):
    if player.x == asteroid.x and player.y == asteroid.y:
        return True
    return False


def main():
    timeout = time.time() + TIMEOUT
    curses.initscr()
    win = curses.newwin(HEIGHT, WIDTH, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    player = Player()
    win.addch(player.y, player.x, '^')

    key = None
    asteroids = []

    curr_time = time.time()

    while True:
        if time.time() > timeout:
            break
        win.border(0)
        win.addstr(0, 0, 'Time Left : {:.2f} '.format(timeout-time.time()))
        #win.timeout(int(time.time()-timeout))

        event = win.getch()
        key = None if event == -1 else event

        if key == ord('a'):
            player.left()
            win.addch(player.y, player.x, '^')
            win.addch(player.y, player.x+1, ' ')
        elif key == ord('d'):
            player.right()
            win.addch(player.y, player.x, '^')
            win.addch(player.y, player.x-1, ' ')

        if time.time() > curr_time+1:
            aster = Asteroid()
            asteroids.append(aster)
            for asteroid in asteroids:
                asteroid.fall()
                if asteroid.exist:
                    win.addch(asteroid.y, asteroid.x, '@')
                    win.addch(asteroid.y-1, asteroid.x, ' ')
                if hit(player, asteroid):
                    win.addch(asteroid.y, asteroid.x, '*')
            curr_time = time.time()

    curses.endwin()

if __name__ == '__main__':
    main()
