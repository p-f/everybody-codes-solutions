#!/bin/env python3

from itertools import count, cycle

def _read(path: str) -> list[tuple[int, int]]:
  res: list[tuple[int, int]] = []
  with open(path, "r") as handle:
    while l := handle.readline():
      exp, base = l[4:].split(" ")
      res.append((int(exp), int(base)))
  return res

def part1():
  res: int = 0
  for l, r in _read("03-part1.txt"):
    line_res: int = 0
    exp: int = 0
    while l or r:
      line_res += (r % 10) * ((l % 10) ** exp)
      l //= 10
      r //= 10
      exp += 1
    res += line_res
  print("Part 1:", res)

def part2():
  res: int = 0
  with open("03-part2.txt", "r") as handle:
    while line := handle.readline():
      l, r = line[4:].split()
      exp: int = 0
      line_res: int = 0
      for std, base in zip(cycle(reversed(l)), (reversed(r))):
        line_res += int(base) * (int(std) ** exp)
        exp += 1
      res += line_res
  print("Part 2:", res)

def _find_min(goal: int, factors: list[int]) -> int:
  for base in count():
    res = 0
    digit = 0
    coeff = base
    while coeff:
      res += factors[digit] * (coeff % 10)
      digit += 1
      coeff //= 10
    if res == goal:
      return base
  return -1

def part3():
  res: int = 0
  with open("03-part3.txt", "r") as handle:
    while line := handle.readline():
      l, r = line[5:].split()
      factors: list[int] = []
      line_res: int = 0
      exp: int = 0
      for std, digit in zip(cycle(reversed(l)), (reversed(r))):
        base: int = int(std) ** exp
        factor: int = int(digit)
        line_res += factor * base
        factors.append(base)
        exp += 1
      if _find_min(line_res, factors) == int(r):
        res += line_res
  print("Part 3:", res)


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()