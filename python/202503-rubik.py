#!/usr/bin/python3

from copy import deepcopy
from itertools import product
from math import ceil
import os
from random import choice
import sys
# WARNING: termcolor f1c08c36e33d1223062ce6c44f5ee2094eddbfe2 fixed missing black, but
# wsl still uses ancient 22.04 ubuntu, and the buggy version of termcolor will be around
# for decades apparently, thanks to Microsoft. So let's not use black, let's use grey!
from termcolor import colored, COLORS, HIGHLIGHTS
# Have to get rid of termcolor completely, buggy, API changing, piece of ...
COLORS['light_yellow'] = 93
COLORS['light_grey'] = 37
COLORS['white'] = 97
HIGHLIGHTS['on_light_grey'] = 47

import termios
import time
import tty

# By increasing stdout buffer, we reduce flickering, because only
# sys.stdout.flush will talk to the terminal in one big batch.
sys.stdout = open(1, "w", buffering = 10485760)

class ReadOrResize():
    def __init__(self):
        import signal
        import socket
        import selectors

        # Reopen stdin unbuffered binary, because otherwise if the user
        # is pressing buttons faster than the animation, then our selector
        # gets stuck.
        sys.stdin = os.fdopen(0, buffering=0, mode='rb')

        self.read, self.write = socket.socketpair()
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.read, selectors.EVENT_READ)
        self.selector.register(sys.stdin, selectors.EVENT_READ)
        self.handler = lambda _signal, _frame: self.tick()
        signal.signal(signal.SIGWINCH, self.handler)

    def tick(self):
        self.write.send(b'\0')

    def readOrResize(self):
        for key, _ in self.selector.select():
            if key.fileobj == sys.stdin:
                return sys.stdin.read(1).decode('ascii')
            else:
                self.read.recv(1)
                return "resize"

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

def strcursorleft(i):
    return chr(27) + f'[{i}D'

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
        self.steps = 0
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'W' * 3 + ' ' * 6, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray('O' * 3 + 'G' * 3 + 'R' * 3 + 'B' * 3, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'Y' * 3 + ' ' * 6, encoding = 'ascii'))

    # Very hacky API: if begin is True, we return a tuple, where the second item is how many tiles to skip from the cube
    def instruction(self, row, rowrepeat, begin):
        match row, rowrepeat, begin:
            case 3, 0, True:
                return 'u ', 0
            case 3, 0, False:
                return ' i'
            case (4, 0, True):
                return 'a ', 0
            case (4, 1, True):
                return '◀◀', 0
            case (4, 0, False):
                return ' d'
            case (4, 1, False):
                return '▶▶'
            case 5, 1, True:
                return 'j ', 0
            case 5, 1, False:
                return ' k'
            case 0, 0, True:
                msg = '  Front   - m '
                return msg, 2
            case 0, 1, True:
                msg = "  Front'  - n "
                return msg, 2
            case 0, 2, True:
                msg = '  Back    - 7 '
                return msg, 2
            case 1, 0, True:
                msg = "  Back'   - 8 "
                return msg, 2
            case 1, 2, True:
                msg = "  Sexy    - ouli    "
                return msg, 3
            case 2, 0, True:
                msg = "  Sexy'   - uoil    "
                return msg, 3
            case 6, 1, True:
                msg = '  Slower  - + '
                return msg, 2
            case 6, 2, True:
                msg = '  Faster  - - '
                return msg, 2
            case 7, 1, True:
                msg = '  Shuffle - N '
                return msg, 2
            case 7, 2, True:
                msg = '  Undo    - x '
                return msg, 2
            case 8, 2, True:
                msg = '  Quit    - Q '
                return msg, 2
            case _, _, True:
                return '  ', 0
            case _, _, False:
                return '  '

    def draw(self):
        w, h = os.get_terminal_size()
        dw, dh = 75, 30
        vpad = int((h - dh) / 2)
        hpad = ' ' * ceil((w - dw) / 2)
        cursorhome()
        for _ in range(vpad):
            pr(' ' * w)
            nextline()
        pr(hpad + colored('                     y/z  ▲ w ▲   o                                        ', 'grey', 'on_light_grey') + hpad)
        nextline()
        for ri in range(len(self.state)):
            r = self.state[ri]
            for repeat in range(3):
                instruction, instruction_skip = self.instruction(ri, repeat, True)
                pr(hpad + colored(instruction, 'grey', 'on_light_grey'))
                for c in r[instruction_skip:]:
                    if repeat == 0:
                        colorchar('▇▇▇▇▇ ', c)
                    if repeat == 1:
                        colorchar('█████ ', c)
                    if repeat == 2:
                        colorchar('▀▀▀▀▀ ', c)
                pr(strcursorleft(1) + colored(self.instruction(ri, repeat, False), 'grey', 'on_light_grey') + hpad)
                nextline()

        pr(hpad + colored(f'                      h   ▼ s ▼   l               {self.steps:4d} Steps   {f"Anim: {self.anim:.2f}s "}', 'grey', 'on_light_grey') + hpad)
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
        self.steps += 1
        self.rotatestate(uprow, 1 * mul)
        for i in range(2):
            self.rotatestate(uprow, 1 * mul, False)
            self.rotatestate(upside, -1 * mul)

    def down(self, mul = 1):
        self.steps += 1
        self.rotatestate(downrow, -1 * mul)
        for i in range(2):
            self.rotatestate(downrow, -1 * mul, False)
            self.rotatestate(downside, -1 * mul)

    def right(self, mul = 1):
        self.steps += 1
        self.rotatestate(rightcol, 1 * mul)
        for i in range(2):
            self.rotatestate(rightcol, 1 * mul, False)
            self.rotatestate(rightside, -1 * mul)

    def left(self, mul = 1):
        self.steps += 1
        self.rotatestate(leftcol, 1 * mul)
        for i in range(2):
            self.rotatestate(leftcol, 1 * mul, False)
            self.rotatestate(leftside, 1 * mul)

    def front(self, mul = 1):
        self.steps += 1
        self.rotatestate(frontcirc, 1 * mul)
        for i in range(2):
            self.rotatestate(frontcirc, 1 * mul, False)
            self.rotatestate(frontside, 1 * mul)

    def back(self, mul = 1):
        self.steps += 1
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
# Have to use termios.tcgetattr instead of trusting return of tty.setcbreak (python 3.12 is still too new).
tty_attrs = termios.tcgetattr(1)
tty.setcbreak(1)
clearscreen()
wrapoff()

try:
    readOrResize = ReadOrResize()
    cube = Cube()
    undo = []
    while True:
        cube.draw()
        key = readOrResize.readOrResize()
        match key:
            case 'x':
                if len(undo) >= 1:
                    cube.state = undo.pop()
                    cube.steps -= 1
            case 'Q':
                break
            case 'u':
                undo.append(cube.state)
                cube.up()
            case 'i':
                undo.append(cube.state)
                cube.up(-1)
            case 'k':
                undo.append(cube.state)
                cube.down()
            case 'j':
                undo.append(cube.state)
                cube.down(-1)
            case 'o':
                undo.append(cube.state)
                cube.right()
            case 'l':
                undo.append(cube.state)
                cube.right(-1)
            case 'y' | 'z':
                undo.append(cube.state)
                cube.left()
            case 'h':
                undo.append(cube.state)
                cube.left(-1)
            case 'n':
                undo.append(cube.state)
                cube.front()
            case 'm':
                undo.append(cube.state)
                cube.front(-1)
            case '7':
                undo.append(cube.state)
                cube.back()
            case '8':
                undo.append(cube.state)
                cube.back(-1)
            case 'd':
                cube.cuberight()
            case 'a':
                cube.cuberight(-1)
            case 'w':
                cube.cubeup()
            case 's':
                cube.cubeup(-1)
            case '+' | '=':
                cube.anim += 0.01
            case '-' | '_':
                cube.anim -= 0.01
                cube.anim = max(cube.anim, 0)
            case 'N':
                shuffle = list(product([cube.left, cube.front, cube.right, cube.up, cube.down, cube.back], [-1, 1, 2]))
                oldanim = cube.anim
                cube.anim = 0
                for s in range(400):
                    f, i = choice(shuffle)
                    f(i)
                cube.anim = oldanim
                undo = []
                cube.steps = 0

finally:
    # restore input buffering
    termios.tcsetattr(1, termios.TCSAFLUSH, tty_attrs)
    wrapon()
    sys.stdout.flush()
