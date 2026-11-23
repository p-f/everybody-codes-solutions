#!/bin/env python3

from itertools import pairwise

def _read(file: str) -> list[str]:
  res: list[str] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      res.append(l.strip())
  return res

def part1():
  grid: list[str] = _read("14-part1.txt")
  cols = len(grid[0])
  bind: int = 0
  for row in grid:
    bind += 2 + sum(l != r for l, r in pairwise(row))
  for c in range(cols):
    bind += 2 + sum(l[c] != r[c] for l, r in pairwise(grid))
  print("Part 1", bind, sep="\t")

  
def main():
  part1()
  # part2()
  # part3()


if __name__ == "__main__":
  main()