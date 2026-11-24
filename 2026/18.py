#!/bin/env python3

from itertools import pairwise

type Rule = tuple[int, int]

def _read(file: str) -> list[Rule]:
  lines: list[Rule] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      x, y = map(lambda p: int(p.split("=")[1]), l.split())
      lines.append((x, y,))
  return lines

def _compress_rules(rules: list[Rule]) -> list[Rule]:
  rules.sort()
  changed: bool = True
  while changed:
    changed = False
    # Pass left to right
    for left in range(len(rules)):
      left_height: int = rules[left][1]
      right: int = left
      for right_candidate in range(left + 1, len(rules)):
        right_height: int = rules[right_candidate][1]
        if right_height == left_height:
          right = right_candidate
        elif right_height > left_height:
          right = right_candidate
          break # Cannot continue
      if right > (left + 1):
        changed = True
        del rules[left + 1: right]
        break
    if changed: continue
    # Pass right to left
    for right in range(len(rules) - 1, -1, -1):
      right_height: int = rules[right][1]
      left: int = right
      for left_candidate in range(right - 1, -1, -1):
        left_height: int = rules[left_candidate][1]
        if left_height == right_height:
          left = left_candidate
        elif left_height > right_height:
          left = left_candidate
          break
      if left < (right - 1):
        changed = True
        del rules[left + 1: right]
        break
  return rules

def _total_heights(rules: list[Rule]) -> int:
  area: int = sum(r[1] for r in rules)
  for (xl, yl), (xr, yr) in pairwise(rules):
    area += (xr - xl - 1) * min(yl, yr)
  return area

def part1():
  rules: list[Rule] = _read("18-part1.txt")
  rules = _compress_rules(rules)
  area: int = _total_heights(rules)
  print("Part 1:", area)

type RuleW = tuple[int, int, int]

def _read2(file: str) -> list[RuleW]:
  lines: list[RuleW] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      x, y, w = map(lambda p: int(p.split("=")[1]), l.split())
      lines.append((x, y, w,))
  return lines

def _part2(filepath: str) -> int:
  rules: list[RuleW] = _read2(filepath)
  rules_expanded: list[Rule] = []
  for (x, y, w) in rules:
    rules_expanded.append((x, y,))
    if w > 1:
      rules_expanded.append((x + w - 1, y,))
  rules_expanded = _compress_rules(rules_expanded)
  area: int = _total_heights(rules_expanded)
  return area

def part2():
  area: int = _part2("18-part2.txt")
  print("Part 2:", area)

def part3():
  area: int = _part2("18-part3.txt")
  print("Part 3:", area)

def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()