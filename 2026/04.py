#!/bin/env python3

from collections import Counter

def _read(path: str):
  with open(path, "r") as handle:
    while l:= handle.readline():
      yield map(int, map(lambda p: p.split("=")[1], l.split()))

def part1():
  per_participant: dict[int, int] = Counter()
  for id, _, _, time in _read("04-part1.txt"):
    per_participant[id] += time
  res = 0
  for i, t in enumerate(sorted(per_participant.values())):
    res += (i + 1) * t
  print("Part 1:", res)


def main():
  part1()


if __name__ == "__main__":
  main()