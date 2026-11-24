#!/bin/env python3

type Rule = tuple[int, int]

def _read(file: str) -> list[Rule]:
  lines: list[Rule] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      x, y = map(lambda p: int(p.split("=")[1]), l.split())
      lines.append((x, y,))
  return lines

def _get_heights(rules: list[Rule]) -> list[int]:
  heights: list[int] = [0] * (rules[-1][0] + 1)
  def _fill(x1: int, x2: int, height: int):
    step: int = 1 if x2 > x1 else -1
    for x in range(x1, x2 + step, step):
      heights[x] = max(height, heights[x])
  for (x, y) in rules:
    for (x_other, y_other) in rules:
      if y_other >= y:
        _fill(x, x_other, y)
  return heights

def part1():
  rules: list[Rule] = _read("18-part1.txt")
  heights: list[int] = _get_heights(rules)
  print("Part 1:", sum(heights))

type RuleW = tuple[int, int, int]

def _read2(file: str) -> list[RuleW]:
  lines: list[RuleW] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      x, y, w = map(lambda p: int(p.split("=")[1]), l.split())
      lines.append((x, y, w,))
  return lines

def part2():
  rules: list[RuleW] = _read2("18-part2.txt")
  rules_expanded: list[Rule] = []
  for (x, y, w) in rules:
    rules_expanded.append((x, y,))
    if w > 1:
      rules_expanded.append((x + w - 1, y,))
  heights: list[int] = _get_heights(rules_expanded)
  print("Part 2:", sum(heights))

def main():
  part1()
  part2()
  # part3()

if __name__ == "__main__":
  main()