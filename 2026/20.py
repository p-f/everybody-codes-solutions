#!/bin/env python3

from typing import Callable
from operator import add, sub

def _read(file: str) -> list[list[str]]:
  lines: list[list[str]] = []
  with open(file, "r") as handle:
    while l := handle.readline():
      lines.append(l.strip().split())
  return lines

_OPS: dict[str, Callable[[int, int], int]] = {
  "+": add,
  "-": sub
}

_SEQ_COUNTS: tuple[int, ...] = (6, 2, 5, 5, 4, 5, 6, 3, 7, 6)

def _seq_count(v: int | str) -> int:
  if isinstance(v, int):
    return _SEQ_COUNTS[v]
  elif v == '+':
    return 2
  elif v == '-':
    return 1
  else:
    raise ValueError(v)

def part1():
  equations: list[list[str]] = _read("20-part1.txt")
  res: int = 0
  for left1, op1, right1, _, left2, op2, righ2 in equations:
    nl1, nr1, nl2, nr2 = int(left1), int(right1), int(left2), int(righ2)
    if _OPS[op1](nl1, nr1) != _OPS[op2](nl2, nr2): continue
    res += 2 + _seq_count(nl1) + _seq_count(nr1) + _seq_count(nl2) + _seq_count(nr2) + _seq_count(op1) + _seq_count(op2)
  print("Part 1:", res, sep="\t")


def main():
  part1()
  # part2()
  # part3()

if __name__ == "__main__":
  main()