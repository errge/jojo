#!/usr/bin/python3

import math

def run():
    mi = 1
    ma = 2
    for i in range(40):
        kozep = mi + ma
        kozep /= 2
        if kozep*kozep > 2:
            ma = kozep
        else:
            mi = kozep
        print(f"{kozep:.12f}, {abs(kozep-math.sqrt(2)):.12f}")

run()
