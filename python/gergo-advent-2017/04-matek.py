from math import sqrt

input = 2651490

lower_square_number_root = int(sqrt(input))
if lower_square_number_root % 2 == 0:
    but_smallereq_odd = lower_square_number_root - 1
else:
    but_smallereq_odd = lower_square_number_root

# middles = (lower_square_number_root + 1)  [1,2,3,4]

n = but_smallereq_odd

start = n*n + 1 + (n-1) // 2
while input >= start:
    start += n+1
start -= n+1

steps = input - start
steps += (n + 1) // 2

print(steps)
