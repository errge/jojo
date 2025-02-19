gamelen, input = 256, [83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100]
# gamelen, input = 5, [0, 3, 4, 1, 5]

list, skip, jumptotal = list(range(gamelen)), 0, 0
while input:
    inp = input.pop(0)
    print(f'Start           : {list}')
    if inp > 0: list[:inp] = list[inp-1::-1]   # Corner-case only in big input: inp == 0
    print(f'Reversed first {inp}: {list}')
    jump = (inp+skip) % gamelen
    list = list[jump:] + list[:jump]
    print(f'Reorder first   : {list}')
    jumptotal += jump
    jumptotal %= gamelen
    print(f'Order back: {gamelen - jumptotal}')
    print('----')
    skip += 1

jumpback = gamelen - jumptotal
list = list[jumpback:] + list[:jumpback]
print(list)
print(list[0] * list[1])
