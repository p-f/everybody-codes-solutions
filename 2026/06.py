#!/bin/env python3

from collections.abc import Generator

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
  print("Part 3:", len(seen) - 1)


def main():
  part1()


if __name__ == "__main__":
  main()