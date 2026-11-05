#!/bin/env python3

from collections import Counter
from typing import NamedTuple

class Plant(NamedTuple):
  id: int
  growth: int
  limit: int

def _read(path: str) -> list[Plant]:
  rules: list[Plant] = []
  with open(path, "r") as h:
    while l := h.readline():
      rules.append(Plant(*map(lambda p: int(p.split("=")[1]), l.strip().split(", "))))
  return rules


def part1():
  plants: list[Plant] = _read("09-part1.txt")
  res: int = 0
  for p in plants:
    # print(p)
    branches: list[int] = [0]
    total: int = 0
    time: int = 0
    while total < p.limit:
      time += 1
      next: list[int] = []
      for b in branches:
        bb = b + 1
        if bb == p.growth:
          next.append(bb // 2)
          next.append(bb // 2)
          next.append(1)
          total += 2
        else:
          next.append(bb)
          total += 1
      branches = next
      # print(branches, "time", time, "total", total)
    res += time
    # print(p, "res", time)
  # print(plants)
  print("Part 1", res)


def grow(infile: str) -> int:
  plants: list[Plant] = _read(infile)
  res: int = 0
  for p in plants:
    # print(p)
    if p.limit == 1:
      res += 1
      continue
    branches: Counter[int] = Counter([0])
    leaves: int = 1
    time: int = 0
    while leaves < p.limit:
      steps: int = max(p.growth - max(branches), 1)
      time += steps
      next: Counter[int] = Counter()
      for b, count in branches.items():
        bb = b + steps
        if bb == p.growth:
          next[bb // 2] += 2 * count
          next[1] += count
          leaves += count
        else:
          next[bb] += count
      branches = next
      # print(branches, "time", time, "total", leaves)
    res += time
    # print(p, "res", time)
  # print(plants)
  return res

def main():
  part1()
  print("Part 2", grow("09-part2.txt"))
  print("Part 3", grow("09-part3.txt"))

if __name__ == "__main__":
  main()