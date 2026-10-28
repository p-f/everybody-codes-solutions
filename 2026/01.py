#!/bin/env python3

from bisect import bisect_left
from collections.abc import Generator


def _read_input() -> Generator[int, None, None]:
  with open("01-part3.txt", "r") as handle:
    return map(int, handle.readline().split(","))

def main():
  last_base: int = 1
  squares: list[int] = [1]
  res: int = 0
  for cones in _read_input():
    while cones > squares[-1]:
      last_base += 1
      squares.append(last_base * last_base)
    next_size = squares[bisect_left(squares, cones)]
    res += next_size - cones
  print("Part 1", res, sep="\t")
  # Part 2
  last_base = 3
  frames: list[int] = [8]
  res = 0
  for cones in _read_input():
    while cones > frames[-1]:
      last_base += 1
      frames.append(4 * last_base - 4)
    next_size = frames[bisect_left(frames, cones)]
    res += next_size - cones
  print("Part 2:", res, sep="\t")
  # Part 3
  last_base = 3
  frames: list[int] = [8]
  res = 0
  for cones in _read_input():
    while cones > frames[-1]:
      last_base += 2
      frames.append(last_base * last_base - 1)
    next_size = frames[bisect_left(frames, cones)]
    res += next_size - cones
  print("Part 3:", res, sep="\t")


if __name__ == "__main__":
  main()