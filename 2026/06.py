#!/bin/env python3

from collections import defaultdict
from functools import cache

def _read(path: str) -> dict[str, list[str]]:
  res: dict[str, list[str]] = dict()
  with open(path, "r") as handle:
    while l:= handle.readline():
      s, d = l.strip().split(":")
      res[s] = list(d.split(","))
  return res


def part1():
  incr = _read("06-part1.txt")
  seen: set[str] = {"NULL"}
  queue = ["NULL"]
  while queue:
    current = queue.pop(0)
    for next in incr.get(current, ()):
      if next not in seen:
        seen.add(next)
        queue.append(next)
  print("Part 1:", len(seen) - 1)

def _inv_incredients(recipe: dict[str, list[str]]) -> dict[str, set[str]]:
  uses: dict[str, set[str]] = defaultdict(set)
  for k, v in recipe.items():
    for vv in v:
      uses[vv].add(k)
  return uses

def _find_uses(uses: dict[str, set[str]], of: str) -> set[str]:
  seen: set[str] = {of}
  queue: list[str] = [of]
  while queue:
    current = queue.pop(0)
    for next in uses[current]:
      if next not in seen:
        seen.add(next)
        queue.append(next)
  return seen


def part2():
  incr = _read("06-part2.txt")
  uses = _inv_incredients(incr)
  seen: set[str] = _find_uses(uses, "NULL")
  print("Part 2:", len(seen) - 1)


def part3():
  incr = _read("06-part3.txt")
  uses = _inv_incredients(incr)
  seen1 = _find_uses(uses, "NULLv1")
  seen2 = _find_uses(uses, "NULLv2")
  seen3 = _find_uses(uses, "NULLv3")
  res = seen1.intersection(seen2) | seen1.intersection(seen3) | seen2.intersection(seen3)
  print("Part 3", len(res - {"NULLv1", "NULLv2", "NULLv3"}))
    

def main():
  part1()
  part2()
  part3()


if __name__ == "__main__":
  main()