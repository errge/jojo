#!/usr/bin/python3

security = {}

with open('13.txt', 'r') as f:
    for l in f.readlines():
        inp = l.split(": ")
        security[int(inp[0])] = int(inp[1])

invoice = 0
for pico in security.keys():
    if pico % ((security[pico] - 1) * 2) == 0:
        invoice += pico * security[pico]

print(invoice)
