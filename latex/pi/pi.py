#!/usr/bin/python3

from math import sqrt, pi

def felezo(BC):
  BX = BC / 2
  AX = sqrt(1 - BX * BX)
  XY = 1 - AX
  BY = sqrt(BX * BX + XY * XY)
  return BY

def run():
  BC = 1
  szogszam = 6
  for i in range(20):
    kerulet = BC * szogszam
    print(f"{i+1:2d}. {szogszam:8d}-szög kerülete: {kerulet:.12f}, pi: {kerulet/2:.15f}")
    BC = felezo(BC)
    szogszam *= 2

run()
print()
print(f"Igazi Pi:                                       {pi}")
