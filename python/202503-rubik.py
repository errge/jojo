#!/usr/bin/python3

from copy import deepcopy
from itertools import product
from math import ceil
import os
from random import choice
import sys
from termcolor import colored
import termios
import time
import tty

def pr(str):
    print(str, end = '')

# Good VT100 description: http://www.braun-home.net/michael/info/misc/VT100_commands.htm
def cursorhome():
    pr(chr(27) + '[H')

def clearscreen():
    pr(chr(27) + '[2J')

def wrapoff():
    pr(chr(27) + '[?7l')

def wrapon():
    pr(chr(27) + '[?7h')

def nextline():
    # A very safe next line: go one line down and 1000 characters to the left.
    # But all these movement commands NEVER scroll (not even on the last line).
    # So we can accidentally overrun, and still no flickering of the screen.
    pr(chr(27) + '[1B' + chr(27) + '[1000D')

colors = {
    'W': 'white',
    'G': 'green',
    'O': 'yellow',
    'Y': 'light_yellow',
    'R': 'red',
    'B': 'blue',
    ' ': 'light_grey',
}

def colorchar(char, color):
    pr(colored(char, colors[chr(color)], 'on_light_grey'))

upside    = [(0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2,4), (2, 3), (1, 3)]
uprow     = [(3, x) for x in range(12)]
midrow    = [(4, x) for x in range(12)]
midcol    = [(y, 4) for y in range(9)] + [(5, 10), (4, 10), (3, 10)]
downrow   = [(5, x) for x in range(12)]
downside  = [(y + 6, x) for (y, x) in upside]
rightside = [(3, 6), (3, 7), (3, 8), (4, 8), (5, 8), (5, 7), (5, 6), (4, 6)]
rightcol  = [(y, 5) for y in range(9)] + [(5, 9), (4, 9), (3, 9)]
leftside  = [(y, x - 6) for (y, x) in rightside]
leftcol   = [(y, 3) for y in range(9)] + [(5, 11), (4, 11), (3, 11)]
frontside = [(3, 3), (3, 4), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (4, 3)]
frontcirc = [(2, 3), (2, 4), (2, 5), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (5, 2), (4, 2), (3, 2)]
backside  = [(y, x + 6) for (y, x) in frontside]
backcirc  = [(0, 3), (0, 4), (0, 5), (3, 8), (4, 8), (5, 8), (8, 5), (8, 4), (8, 3), (5, 0), (4, 0), (3, 0)]

class Cube:
    def __init__(self):
        self.my = 2
        self.anim = 0.05
        self.state = []
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'W' * 3 + ' ' * 6, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray('O' * 3 + 'G' * 3 + 'R' * 3 + 'B' * 3, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'Y' * 3 + ' ' * 6, encoding = 'ascii'))

    def draw(self):
        w, h = os.get_terminal_size()
        dw, dh = 63, 20
        vpad = int((h - dh) / 2)
        hpad = ' ' * ceil((w - dw) / 2)
        cursorhome()
        for _ in range(vpad):
            pr(' ' * w)
            nextline()
        pr(colored(hpad + '█' * dw + hpad, 'light_grey'))
        nextline()
        for r in self.state:
            for repeat in range(2):
                pr(colored(hpad + '██', 'light_grey'))
                for c in r:
                    if repeat == 0:
                        colorchar('▇▇▇▇ ', c)
                    if repeat == 1:
                        colorchar('🮆🮆🮆🮆 ', c)
                pr(colored('█', 'light_grey') + hpad)
                nextline()

        # pr(hpad + colored(f'{f"Height: {h}, Width: {w} ":>{dw}}', 'black', 'on_light_grey') + hpad)
        pr(hpad + colored(f'{f"Anim speed: {self.anim:.2f}s ":>{dw}}', 'black', 'on_light_grey') + hpad)
        for _ in range(vpad + 1):
            nextline()
            pr(' ' * w)
        sys.stdout.flush()

    def rotatestate(self, how, howmuch, anim = True):
        newstate = deepcopy(self.state)
        for i in range(len(how)):
            y, x = how[i]
            y_, x_ = how[(i+howmuch) % len(how)]
            newstate[y][x] = self.state[y_][x_]
        self.state = newstate
        if anim:
            self.draw()
            time.sleep(self.anim)

    def up(self, mul = 1):
        self.rotatestate(uprow, 1 * mul)
        for i in range(2):
            self.rotatestate(uprow, 1 * mul, False)
            self.rotatestate(upside, -1 * mul)

    def down(self, mul = 1):
        self.rotatestate(downrow, -1 * mul)
        for i in range(2):
            self.rotatestate(downrow, -1 * mul, False)
            self.rotatestate(downside, -1 * mul)

    def right(self, mul = 1):
        self.rotatestate(rightcol, 1 * mul)
        for i in range(2):
            self.rotatestate(rightcol, 1 * mul, False)
            self.rotatestate(rightside, -1 * mul)

    def left(self, mul = 1):
        self.rotatestate(leftcol, 1 * mul)
        for i in range(2):
            self.rotatestate(leftcol, 1 * mul, False)
            self.rotatestate(leftside, 1 * mul)

    def front(self, mul = 1):
        self.rotatestate(frontcirc, 1 * mul)
        for i in range(2):
            self.rotatestate(frontcirc, 1 * mul, False)
            self.rotatestate(frontside, 1 * mul)

    def back(self, mul = 1):
        self.rotatestate(backcirc, 1 * mul)
        for i in range(2):
            self.rotatestate(backcirc, 1 * mul, False)
            self.rotatestate(backside, -1 * mul)

    def cuberight(self, mul = 1):
        for i in range(3):
            if i: self.rotatestate(upside, 1 * mul, False)
            if i: self.rotatestate(downside, -1 * mul, False)
            self.rotatestate(uprow, -1 * mul, False)
            self.rotatestate(midrow, -1 * mul, False)
            self.rotatestate(downrow, -1 * mul)

    def cubeup(self, mul = 1):
        for i in range(3):
            if i: self.rotatestate(leftside, 1 * mul, False)
            if i: self.rotatestate(rightside, -1 * mul, False)
            self.rotatestate(leftcol, 1 * mul, False)
            self.rotatestate(midcol, 1 * mul, False)
            self.rotatestate(rightcol, 1 * mul)

# cbreak mode means, that we read characters from the terminal wo waiting for newline
tty_attrs = tty.setcbreak(1)
clearscreen()
wrapoff()

todo = []
try:
    cube = Cube()
    undo = []
    while True:
        cube.draw()
        undo.append(cube.state)
        if todo:
            key = todo.pop(0)
        else:
            key = sys.stdin.read(1)
        match key:
            case 'z':
                if len(undo) >= 2:
                    undo.pop()
                    cube.state = undo.pop()
            case 'Q':
                break
            case 'u':
                cube.up()
            case 'i':
                cube.up(-1)
            case 'k':
                cube.down()
            case 'j':
                cube.down(-1)
            case 'o':
                cube.right()
            case 'l':
                cube.right(-1)
            case 'y':
                cube.left()
            case 'h':
                cube.left(-1)
            case 'n':
                cube.front()
            case 'm':
                cube.front(-1)
            case '7':
                cube.back()
            case '8':
                cube.back(-1)
            case 'd':
                cube.cuberight()
            case 'a':
                cube.cuberight(-1)
            case 'w':
                cube.cubeup()
            case 's':
                cube.cubeup(-1)
            case '+':
                cube.anim += 0.01
            case '-':
                cube.anim -= 0.01
                cube.anim = max(cube.anim, 0)
            case 'N':
                shuffle = list(product(['L', 'F', 'U', 'D', 'B'], [-1, 1, 2]))
                for s in range(20):
                    match choice(shuffle):
                        case ('L', i):
                            cube.left(i)
                        case ('R', i):
                            cube.right(i)
                        case ('F', i):
                            cube.front(i)
                        case ('B', i):
                            cube.back(i)
                        case ('U', i):
                            cube.up(i)
                        case ('D', i):
                            cube.down(i)

finally:
    # restore input buffering
    termios.tcsetattr(1, termios.TCSAFLUSH, tty_attrs)
    wrapon()
    sys.stdout.flush()
