import sys

input = 265149

spiral = {}

x = 0
y = 0
spiral[(x, y)] = 1

def fill():
    global x, y, spiral, input
    next = 0
    for xx in [-1, 0, 1]:
        for yy in [-1, 0, 1]:
            if (x + xx, y + yy) in spiral:
                next += spiral[(x + xx, y + yy)]
    spiral[(x,y)] = next
    if next > input:
        print(next)
        sys.exit(0)


steps = 0
while True:
    steps += 1
    for i in range(steps):
        x += 1
        fill()
    for i in range(steps):
        y += 1
        fill()
    steps += 1
    for i in range(steps):
        x -= 1
        fill()
    for i in range(steps):
        y -= 1
        fill()
    print(x, y)
    if x < -3:
        break

def draw(spiral, n):
    for y in range(n, -n-1, -1):
        for x in range(-n, n+1):
            print(f'{spiral[(x, y)]:5d}', end = ' ')
        print()

draw(spiral, 2)
