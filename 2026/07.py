#!/bin/env python3

from collections import Counter
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

def _propagate(rules: list[Rule], initial: int) -> int:
  energies: list[int] = [r[1] for r in rules]
  current: Counter[int] = Counter([max(rules, key=lambda r: len(r[2]))[0] - 1])
  energy: int = initial
  while energy:
      next: Counter[int] = Counter()
      for id, count in current.items():
        energies[id] += energy * count
        for out in rules[id][2]:
          next[out - 1] += count
      current = next
      energy -= 1
  return sum(energies)

def part1():
  rules: list[Rule] = _read("07-part1.txt")
  print("Part 1", _propagate(rules, 5))

def part2():
  rules: list[Rule] = _read("07-part2.txt")
  print("Part 2", _propagate(rules, 10))

type IdAndS = tuple[int, int]
def _total_energy(rules: list[Rule], start: int, limit: int = 1000000) -> int:
  energy: list[int] = list(r[1] for r in rules)
  exploded: list[bool] = [False] * len(rules)
  current: Counter[IdAndS] = Counter({(start - 1, 10): 1})
  step = 1
  while current:
    # print("Step", step)
    step += 1
    # print("Pulses\t", current, sep="\t")
    next: Counter[IdAndS] = Counter()
    for (id, pulse), count in current.items():
      if exploded[id]: continue
      energy[id] += pulse * count
      if pulse == 1: continue
      for out in rules[id][2]:
        next[(out - 1, pulse - 1)] += count
    for id in range(len(rules)):
      if energy[id] > limit and not exploded[id]:
        for out in rules[id][2]:
          next[(out - 1, 10)] += 1
        exploded[id] = True
    # print("New energy", *energy, sep="\t")
    current = next
  return sum(e if e < limit else 0 for e in energy)

def part3():
  rules: list[Rule] = _read("07-part3.txt")
  print("Part 3", max(_total_energy(rules, r + 1) for r in range(len(rules))))


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()