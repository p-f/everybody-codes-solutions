#!/bin/env python3

from collections import Counter
from itertools import permutations

type Color = str

def _read(file: str) -> list[list[Color]]:
  lines: list[list[Color]] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      lines.append(list(l.strip()))
  return lines

def _mix(c1: Color, c2: Color) -> Color:
  if c1 == c2: return c1
  elif c1 == 'K' or c2 == 'K': return 'K'
  elif c1 > c2: return _mix(c2, c1)
  elif (c1, c2,) == ('C', 'M'): return 'B'
  elif (c1, c2,) == ('C', 'Y'): return 'G'
  else:
    assert c1 == 'M', c1
    assert c2 == 'Y', c2
    return 'R'

def _separate(colors: list[list[Color]]) -> tuple[list[Color], list[Color]]:
  colors1: list[Color] = []
  colors2: list[Color] = []
  second: bool = False
  for cl in colors:
    if not cl:
      second = True
      continue
    if second:
      colors2 += cl
    else:
      colors1 += cl
  return colors1, colors2

def part1():
  colors: list[list[Color]] = _read("19-part1.txt")
  freq: Counter[Color] = Counter((_mix(*m) for m in zip(*_separate(colors))))
  res: int = 1
  for _, f in freq.most_common(3):
    res *= f
  print("Part 1:", res, sep="\t")

def part2():
  colors: list[list[Color]] = _read("19-part2.txt")
  freq: Counter[tuple[Color, int]] = Counter(((c, int(x)) for c, x in zip(*_separate(colors))))
  max_score: int = 0
  for assignment in permutations("CMYK"):
    freq_assign: Counter[Color] = Counter()
    for (color, variable), com_count in freq.items():
      freq_assign[_mix(color, assignment[variable - 1])] += com_count
    res: int = 1
    for _, f in freq_assign.most_common(3):
      res *= f
    max_score = max(max_score, res)
  print("Part 2:", max_score, sep="\t")


def main():
  part1()
  part2()
  # part3()

if __name__ == "__main__":
  main()