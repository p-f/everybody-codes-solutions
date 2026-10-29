#!/bin/env python3

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


def main():
  part1()


if __name__ == "__main__":
  main()