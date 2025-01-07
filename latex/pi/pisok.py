#!/usr/bin/python3

from mpmath import mpf, workdps, mp, sqrt, nstr, pi
from tqdm import tqdm
from sys import argv, exit, stderr

jegyek = 100000

def felezo(BC):
  BX = BC / 2
  AX = sqrt(1 - BX * BX)
  XY = 1 - AX
  BY = sqrt(BX * BX + XY * XY)
  return BY

def run():
  # Experimental result: we usually need ~1.66 times the number of
  # digits iteration, but this is only a progress bar, this constant
  # doesn't change the result.
  with tqdm(total = int(mp.dps * 1.67)) as pbar:
    BC = mpf(1)
    szogszam = mpf(6)
    most, elozo = None, None
    i = 0
    while True:
      BC = felezo(BC)
      szogszam *= 2
      elozo, most = most, BC * szogszam
      if elozo and most <= elozo:
        break
      pbar.update(1)
      i += 1
    return elozo / 2, i

# +5 might not be enough after a while, but it was definitely enough
# up to 100.000 digits, see piiv.py for safer approach.
with workdps(jegyek + 5):
  mypi_, i = run()
  mypi = nstr(mypi_, jegyek + 5)[2:jegyek + 2]
  mppi = nstr(pi, jegyek + 5)[2:jegyek+2]
  if (mppi != mypi):
    print("Our pi calculation didn't match the official result, sad...", file = stderr)
    exit(1)
  print()
  print()
  print("         3.")
  for index, line in [(i, mypi[i:i + 100]) for i in range(0, len(mypi), 100)]:
    print(f"{index+1:7g}: {line}")
  print()
  print(f"{i} iterations were used")
