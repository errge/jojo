# input = 'se,sw,se,sw,sw'

dirs = input.split(',')
print(dirs)

x, y = 0, 0

tavolsagok = []
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
    xx, yy = abs(x), abs(y)
    newy = yy - xx
    assert(newy % 2 == 0)
    tavolsagok.append(newy // 2 + xx)

print(tavolsagok[-1])
print(max(tavolsagok))
