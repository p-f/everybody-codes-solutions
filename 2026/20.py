#!/bin/env python3

from collections import defaultdict
from typing import Callable
from operator import add, sub
from itertools import product, chain

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
  if isinstance(v, int) or '0' <= v <= '9':
    return _SEQ_COUNTS[int(v)]
  elif v == '+':
    return 2
  elif v == '-':
    return 1
  elif v == '=':
    return 2
  elif v == 'A':
    return 6
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

def int11(s: str) -> int:
  return int(s, base=11)

_DIGITS11: str = "0123456789A"
def int2str11(i: int) -> str:
  if i == 0: return "0"
  digits: list[str] = []
  while i:
    digits.append(_DIGITS11[i % 11])
    i //= 11
  return "".join(reversed(digits))

def part2():
  equations: list[list[str]] = _read("20-part2.txt")
  res: int = 0
  for eq in equations:
    left1, op1, right1, _, left2, op2, righ2 = eq
    nl1, nr1, nl2, nr2 = int11(left1), int11(right1), int11(left2), int11(righ2)
    if _OPS[op1](nl1, nr1) != _OPS[op2](nl2, nr2): continue
    segments: int = sum(_seq_count(c) for part in eq for c in part)
    res += segments
  assert int(int2str11(res), base=11) == res
  print("Part 2:", int2str11(res), sep="\t")

# Characters encoded as binary
#  11
# 2  3
# 2  3
#  44
# 5  6
# 5  6
#  77

_BIN_ENCODE: dict[str, int] = {
  "0": 0b1110111,
  "1": 0b0100100,
  "2": 0b1011101,
  "3": 0b1101101,
  "4": 0b0101110,
  "5": 0b1101011,
  "6": 0b1111011,
  "7": 0b0100101,
  "8": 0b1111111,
  "9": 0b1101111,
  "A": 0b0111111
}

_BIN_DECODE: dict[int, str] = {enc: c for c, enc in _BIN_ENCODE.items()}
assert len(_BIN_ENCODE) == len(_BIN_DECODE)
# Soundness check: segment count
for c, enc in _BIN_ENCODE.items():
  bit_count = enc.bit_count()
  assert _seq_count(c) == bit_count, (c, bit_count)

# Characters that can be turned into other ones by moving 1 segment inside a character
_IN_PLACE_EDITS: dict[str, set[str]] = defaultdict(set)
# Characters that can be turned into other ones by removing 1 segment
_DELETE_EDITS: dict[str, set[str]] = defaultdict(set)
# Characters that can be turned into other ones by inserting 1 segment
_INSERT_EDITS: dict[str, set[str]] = defaultdict(set)

_INSERT_EDITS["-"].add("+")
_DELETE_EDITS["+"].add("-")

for c1, c2 in product(_BIN_ENCODE, repeat=2):
  if c1 == c2: continue
  e1: int = _BIN_ENCODE[c1]
  e2: int = _BIN_ENCODE[c2]
  diffs: int = (e1 ^ e2).bit_count()
  # In-place
  if e1.bit_count() == e2.bit_count() and diffs == 2:
    _IN_PLACE_EDITS[c1].add(c2)
  # By removing 1 character
  if e1.bit_count() - 1 == e2.bit_count() and diffs == 1:
    _DELETE_EDITS[c1].add(c2)
    _INSERT_EDITS[c2].add(c1) # Inverse: adding 1

def _is_equal(equation: list[str], num_len: int) -> bool:
  n1s: str = "".join(equation[0:num_len])
  n2s: str = "".join(equation[num_len + 1:2 * num_len + 1])
  n3s: str = "".join(equation[2 * num_len + 2: 3 * num_len + 2])
  n4s: str = "".join(equation[3 * num_len + 3:])
  opl: str = equation[num_len]
  opr: str = equation[3 * num_len + 2]
  return _OPS[opl](int11(n1s), int11(n2s)) == _OPS[opr](int11(n3s), int11(n4s))

def _can_equalize(equation: list[str], num_len: int) -> list[str]:
  if _is_equal(equation, num_len):
    return equation
  # Try to change a single character
  for i, c in enumerate(equation):
    for alt in _IN_PLACE_EDITS[c]:
      equation[i] = alt
      if _is_equal(equation, num_len):
        return equation
    equation[i] = c
  # Try to move between 2 characters
  for i, c in enumerate(equation):
    for alt_rem in _DELETE_EDITS[c]:
      equation[i] = alt_rem
      for j, cj in enumerate(equation):
        if i == j: continue
        for alt_ins in _INSERT_EDITS[cj]:
          equation[j] = alt_ins
          if _is_equal(equation, num_len):
            return equation
        equation[j] = cj
    equation[i] = c
  return []

def part3(num_len: int = 4):
  equations: list[list[str]] = _read("20-part3.txt")
  res: int = 0
  for eq in equations:
    eq = _can_equalize(list(chain(*eq)), num_len)
    res += sum(_seq_count(c) for c in eq)
  print("Part 3:", int2str11(res), sep="\t")


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()