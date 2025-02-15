import sys

input = 2651490

spiral = {}

x = 0
y = 0
next = 1
spiral[(x, y)] = next
next += 1

def fill():
    global x, y, next, spiral, input
    spiral[(x,y)] = next
    if next == input:
        print(abs(x) + abs(y))
        sys.exit(0)
    next += 1


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

# def draw(spiral, n):
#     for y in range(n, -n-1, -1):
#         for x in range(-n, n+1):
#             print(f'{spiral[(x, y)]:5d}', end = ' ')
#         print()

# draw(spiral, 3)
