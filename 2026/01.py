#!/bin/env python3

from bisect import bisect_left
from collections.abc import Generator


def _read_input() -> Generator[int, None, None]:
  with open("01.txt", "r") as handle:
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
  print(res)
        

if __name__ == "__main__":
  main()