import sys

bytes = sys.stdin.read().encode('ascii')
input = []
for b in bytes:
    input.append(b)
input += [17, 31, 73, 47, 23]
input *= 64

gamelen = 256
list = list(range(gamelen))
skip = 0
jumptotal = 0
while input:
    inp = input.pop(0)
    if inp > 0: list[:inp] = list[inp-1::-1]   # Corner-case only in big input: inp == 0
    reord = (inp+skip) % gamelen
    list = list[reord:] + list[:reord]
    jumptotal += inp+skip
    skip += 1
back = gamelen - jumptotal % gamelen
list = list[back:] + list[:back]
print(list)

while list:
    list16 = list[:16]
    xo = 0
    for l in list16:
        xo ^= l
    print(f'{xo:02x}', end = '')
    list = list[16:]
print()
