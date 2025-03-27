#!/usr/bin/python3

security = {}

with open('13.txt', 'r') as f:
    for l in f.readlines():
        inp = l.split(": ")
        security[int(inp[0])] = int(inp[1])

thistry = 0
while True:
    invoice = 0
    for pico in security.keys():
        if (thistry + pico) % ((security[pico] - 1) * 2) == 0:
            invoice += 1
    if invoice == 0:
        print(thistry)
        break
    thistry += 1
