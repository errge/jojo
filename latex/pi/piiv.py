#!/usr/bin/python3

from mpmath import iv, mpf, mp, ceil, log, nstr
from tqdm import tqdm
from sys import argv, exit, stderr

# Has to be at least 100, or run range has to be increased from 1.7
jegyek = 100000
safety = 10

def felezo(BC):
  BX = BC / 2
  AX = iv.sqrt(1 - BX ** 2)
  XY = 1 - AX
  BY = iv.sqrt(BX ** 2 + XY ** 2)
  return BY

def run():
  # Experimental result: ~1.7 times the number of digits iteration is enough, for sure. :)
  # We check for convergence anyway, so worst case we exit with error...
  BC = iv.mpf('1')
  for i in tqdm(range(int(jegyek * 1.7))):
    elozoBC, BC = BC, felezo(BC)
    # We never seem to be finished under 1.6 times, so this is just an
    # optimization to eliminate unnecessary checks.
    if i > int(jegyek * 1.6):
      elotti = elozoBC * (iv.mpf('6') * 2 ** i) / 2
      utolso = BC * (iv.mpf('6') * 2 ** (i+1)) / 2
      if iv.fabs(elotti - utolso) < iv.mpf('1e-' + str(jegyek + 1)):
        a = str(mpf(elotti.a))[2:jegyek+2]
        b = str(mpf(elotti.b))[2:jegyek+2]
        c = str(mpf(utolso.a))[2:jegyek+2]
        d = str(mpf(utolso.b))[2:jegyek+2]
        if a != b or b != c or c != d:
          print("Result intervals are not the same in the required number of digits, coding error.", file = stderr)
          exit(1)
        return elotti, i
  print("Computation didn't converge, most probably safety is not big enough.", file = stderr)
  exit(1)

iv.dps = jegyek + safety
mp.dps = jegyek + safety
result, i = run()
resultstr = str(mpf(result.a))[2:jegyek+2]
print()
print("All checks passed, result should be trustworthy.")
print()
print("         3.")
for index, line in [(i, resultstr[i:i + 100]) for i in range(0, len(resultstr), 100)]:
  print(f"{index+1:7g}: {line}")
print()
print(f"Safety margin left based on delta: { nstr(-jegyek + abs(log(mpf(result.delta))/log(10)), 4) }.")
print()
print(f"{i} iterations were used")
