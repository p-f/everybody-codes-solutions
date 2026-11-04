#!/bin/env python3

import re

PATTERN: re.Pattern[str] = re.compile("id=([0-9]+), energy=([0-9]+), connections=(.+)")

type Rule = tuple[int, int, list[int]]

def _read(path: str) -> list[Rule]:
  rules: list[Rule] = []
  with open(path, "r") as h:
    while l := h.readline():
      m = PATTERN.match(l.strip())
      assert m, l
      id, energy, connections = m.group(1, 2, 3)
      rules.append((int(id), int(energy), list(map(int, connections.split(",")))))
  return rules

          

def part1():
  rules: list[Rule] = _read("07-part1.txt")
  current: list[int] = [max(rules, key=lambda r: len(r[2]))[0]]
  total: int = 0
  energy: int = 5
  while current and energy:
      total += len(current) * energy
      next: list[int] = []
      for c in current:
        next += rules[c - 1][2]
      current = next
      energy -= 1
  print("Part 1", total + sum(r[1] for r in rules))


def main():
  part1()

if __name__ == "__main__":
  main()