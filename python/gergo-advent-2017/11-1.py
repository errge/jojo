# input = 'se,sw,se,sw,sw'

dirs = input.split(',')
print(dirs)

x, y = 0, 0

for d in dirs:
    match d:
        case 'n':
            y += 2
        case 's':
            y -= 2
        case 'nw':
            x -= 1
            y += 1
        case 'se':
            x += 1
            y -= 1
        case 'ne':
            x += 1
            y += 1
        case 'sw':
            x -= 1
            y -= 1

print(x,y)

x, y = abs(x), abs(y)

newy = y - x
assert(newy % 2 == 0)
print(newy // 2 + x)
