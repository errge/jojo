#!/usr/bin/python3

from copy import deepcopy
from termcolor import colored
import sys
import termios
import time
import tty

def colorchar(char, color):
    if color == ord('W'):
        return colored(char, 'white')
    if color == ord('G'):
        return colored(char, 'green')
    if color == ord('O'):
        return colored(char, 'yellow')
    if color == ord('Y'):
        return colored(char, 'light_yellow')
    if color == ord('R'):
        return colored(char, 'red')
    if color == ord('B'):
        return colored(char, 'blue')
    if color == ord(' '):
        return colored(char, 'light_grey')
    raise Exception(f'wtf {char} {color}')

upside    = [(0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (2,4), (2, 3), (1, 3)]
uprow     = [(3, x) for x in range(12)]
midrow    = [(4, x) for x in range(12)]
midcol    = [(y, 4) for y in range(9)] + [(5, 10), (4, 10), (3, 10)]
downrow   = [(5, x) for x in range(12)]
downside  = [(y+6, x) for (y, x) in upside]
rightside = [(3, 6), (3, 7), (3, 8), (4, 8), (5, 8), (5, 7), (5, 6), (4, 6)]
rightcol  = [(y, 5) for y in range(9)] + [(5, 9), (4, 9), (3, 9)]
leftside  = [(y, x-6) for (y, x) in rightside]
leftcol   = [(y, 3) for y in range(9)] + [(5, 11), (4, 11), (3, 11)]

def rotatestate(state, how, howmuch):
    newstate = deepcopy(state)
    for i in range(len(how)):
        y, x = how[i]
        y_, x_ = how[(i+howmuch) % len(how)]
        newstate[y][x] = state[y_][x_]
    return newstate

class Cube:
    def __init__(self):
        # m for multiplier, mx and my is just for zooming
        self.mx = 4
        self.my = 2
        self.state = []
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'W' * 3 + ' ' * 6, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray('O' * 3 + 'G' * 3 + 'R' * 3 + 'B' * 3, encoding = 'ascii'))
        for i in range(3):
            self.state.append(bytearray(' ' * 3 + 'Y' * 3 + ' ' * 6, encoding = 'ascii'))

    def draw(self):
        print(chr(27) + "[H", end = '')
        print()
        print()
        print()
        print(colored('                ' + '█' * (self.mx * 12 + 2), 'light_grey'))
        for r in self.state:
            for _ in range(self.my):
                print(colored('                █', 'light_grey'), end = '')
                for c in r:
                    print(colorchar('█', c) * self.mx, end = '')
                print(colored('█', 'light_grey'))
        print(colored('                ' + '█' * (self.mx * 12 + 2), 'light_grey'))

    def up(self):
        newstate = rotatestate(self.state, upside, -2)
        newstate = rotatestate(newstate, uprow, 3)
        self.state = newstate

    def down(self):
        newstate = rotatestate(self.state, downrow, -3)
        newstate = rotatestate(newstate, downside, -2)
        self.state = newstate

    def right(self):
        newstate = rotatestate(self.state, rightcol, 3)
        newstate = rotatestate(newstate, rightside, -2)
        self.state = newstate

    def left(self):
        newstate = rotatestate(self.state, leftcol, -3)
        newstate = rotatestate(newstate, leftside, -2)
        self.state = newstate

    def cuberight(self):
        self.up()
        self.up()
        self.up()
        self.down()
        self.state = rotatestate(self.state, midrow, -3)

    def cubeup(self):
        self.right()
        self.left()
        self.left()
        self.left()
        self.state = rotatestate(self.state, midcol, 3)

tty_attrs = tty.setcbreak(1)
print(chr(27) + "[2J", end = '')
try:
    cube = Cube()
    undo = []
    while True:
        cube.draw()
        undo.append(cube.state)
        key = sys.stdin.read(1)
        match key:
            case 'z':
                if len(undo) >= 2:
                    undo.pop()
                    cube.state = undo.pop()
            case '1':
                cube.mx += 1
            case '2':
                cube.my += 1
            case 'Q':
                break
            case 'u':
                cube.up()
            case 'i':
                cube.up()
                cube.up()
                cube.up()
            case 'k':
                cube.down()
            case 'j':
                cube.down()
                cube.down()
                cube.down()
            case 'o':
                cube.right()
            case 'l':
                cube.right()
                cube.right()
                cube.right()
            case 'y':
                cube.left()
                cube.left()
                cube.left()
            case 'h':
                cube.left()
            case 'd':
                cube.cuberight()
            case 'a':
                cube.cuberight()
                cube.cuberight()
                cube.cuberight()
            case 'w':
                cube.cubeup()
            case 's':
                cube.cubeup()
                cube.cubeup()
                cube.cubeup()

finally:
    termios.tcsetattr(1, termios.TCSAFLUSH, tty_attrs)
