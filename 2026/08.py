#!/bin/env python3


def _read(path: str) -> list[list[int]]:
  rules: list[list[int]] = []
  with open(path, "r") as h:
    while l := h.readline():
      rules.append([int(c) if c.isdigit() else 0 for c in l.strip()])
  return rules


def part1():
  grid: list[list[int]] = _read("08-part1.txt")
  rows: int = len(grid)
  cols: int = len(grid[0])
  def scan(row: int, col: int) -> int:
    seen: int = 0
    height: int = -1
    while row < rows and col < cols:
      new_height = grid[row][col]
      if new_height > height:
        height = new_height
        if height != 0:
          # print("Seen height ", height, "at", row, col)
          seen += 1
      height -= 1
      row += 1
      col += 1
    return seen
  reached: int = 0
  for r in range(rows):
    reached += scan(r, 0)
  for c in range(1, cols):
    reached += scan(0, c)
  print("Part 1", reached)

def part2():
  pass

def part3():
  pass


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()