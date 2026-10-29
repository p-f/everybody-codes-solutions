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

def part2():
  per_participant: dict[int, int] = Counter()
  num_participations: dict[int, int] = Counter()
  for id, _, _, time in _read("04-part2.txt"):
    per_participant[id] += time
    num_participations[id] += 1
  res = 0
  part_and_time = [(-num_participations[id], per_participant[id]) for id in per_participant.keys()]
  part_and_time.sort()
  for i, (_, t) in enumerate(part_and_time):
    res += (i + 1) * t
  print("Part 2:", res)

def main():
  part1()
  part2()


if __name__ == "__main__":
  main()