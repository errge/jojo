import sys

gamelen = 256

input = list(sys.stdin.read().encode('ascii'))
input += [17, 31, 73, 47, 23]
input *= 64

list, skip, jumptotal = list(range(gamelen)), 0, 0
while input:
    inp = input.pop(0)
    if inp > 0: list[:inp] = list[inp-1::-1]   # Corner-case only in big input: inp == 0
    jump = (inp+skip) % gamelen
    list = list[jump:] + list[:jump]
    jumptotal += jump
    jumptotal %= gamelen
    skip += 1
jumpback = gamelen - jumptotal
list = list[jumpback:] + list[:jumpback]

while list:
    list16 = list[:16]
    xo = 0
    for l in list16:
        xo ^= l
    print(f'{xo:02x}', end = '')
    list = list[16:]
print()
