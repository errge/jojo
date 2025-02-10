#!/usr/bin/python3

import sys

sys.exit(1)

def increase(x):
    x += 1

i = 42
print(i)
increase(i)
print(i)

sys.exit(1)

def heal(player):
    player['hp'] += 10

jack = {
    'name': 'Jack',
    'hp': 75
}

print(jack)
heal(jack)
print(jack)
