gamelen, input = 256, [83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100]
# gamelen, input = 5, [0, 3, 4, 1, 5]

list = list(range(gamelen))
skip = 0
jumptotal = 0
while input:
    inp = input.pop(0)
    print(f'Start           : {list}')
    if inp > 0: list[:inp] = list[inp-1::-1]   # Corner-case only in big input: inp == 0
    print(f'Reversed first {inp}: {list}')
    reord = (inp+skip) % gamelen
    list = list[reord:] + list[:reord]
    print(f'Reorder first   : {list}')
    jumptotal += inp+skip
    print(f'Order back: {gamelen - jumptotal % gamelen}')
    print('----')
    skip += 1

back = gamelen - jumptotal % gamelen
list = list[back:] + list[:back]
print(list)
print(list[0] * list[1])
