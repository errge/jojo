#!/usr/bin/python3

graf = {}

with open('12.txt', 'r') as f:
    for l in f.readlines():
        ll = list(map(int, filter(lambda x: x != '', ''.join(list(filter(lambda x: x in " 0123456789", l))).split(' '))))
        graf[ll[0]] = ll[1:]

visited = {}

def go(where):
    if where in visited: return
    visited[where] = True
    for i in graf[where]:
        go(i)

go(min(graf.keys()))

print(len(visited))
