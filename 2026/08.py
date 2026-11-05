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
  grid: list[list[int]] = _read("08-part2.txt")
  rows: int = len(grid)
  cols: int = len(grid[0])
  def scan(row: int, col: int, dr: int, dc: int) -> int:
    seen: int = 0
    height: int = -1
    while 0 <= row < rows and 0 <= col < cols:
      new_height = grid[row][col]
      if new_height == 0:
        row += dr
        col += dc
        continue
      if new_height > height:
        height = new_height
        if height != 0:
          # print("Seen height ", height, "at", row, col)
          seen += 1
      height -= 1
      row += dr
      col += dc
    return seen
  reached_total: int = 0
  reached: int = 0
  for r in range(rows):
    reached += scan(r, 0, 1, 1)
  for c in range(1, cols):
    reached += scan(0, c, 1, 1)
  # print("Down right", reached)
  reached_total += reached

  reached = 0
  for r in range(rows):
    reached += scan(r, cols - 1, 1, -1)
  for c in range(cols - 1):
    reached += scan(0, c, 1, -1)
  # print("Down left", reached)
  reached_total += reached

  reached = 0
  for r in range(rows):
    reached += scan(r, cols - 1, 0, -1)
  # print("Left", reached)
  reached_total += reached

  reached = 0
  for r in range(rows):
    reached += scan(r, cols - 1, -1, -1)
  for c in range(cols - 1):
    reached += scan(rows - 1, c, -1, -1)
  # print("Top left", reached)
  reached_total += reached

  reached = 0
  for r in range(rows):
    reached += scan(r, 0, -1, 1)
  for c in range(1, cols):
    reached += scan(rows - 1, c, -1, 1)
  # print("Top right", reached)
  reached_total += reached

  reached = 0
  for r in range(rows):
    reached += scan(r, 0, 0, 1)
  # print("Right", reached)
  reached_total += reached

  print("Part 2", reached_total)


def part3():
  grid: list[list[int]] = _read("08-part3.txt")
  rows: int = len(grid)
  cols: int = len(grid[0])
  def scan(row: int, col: int, dr: int, dc: int) -> int:
    seen: int = 0
    height: int = -1
    while 0 <= row < rows and 0 <= col < cols:
      new_height = grid[row][col]
      if new_height == 0:
        row += dr
        col += dc
        continue
      if new_height > height and new_height > 0:
        height = new_height
        grid[row][col] += 1
        seen += 1
      height -= 1
      row += dr
      col += dc
    return seen
  def check_warriors() -> int:
    w = 0
    for r in range(rows):
      for c in range(cols):
        new: int = grid[r][c]
        match new:
          case 10:
            w += 1
            new = -3
          case -3:
            new = -2
          case -2:
            new = -1
          case -1:
            new = 1
          case _:
            pass
        grid[r][c] = new
    return w
    
  reached_total: int = 0
  warriors: int = 0
  while True:
    reached: int = 0
    for r in range(rows):
      reached += scan(r, 0, 1, 1)
    for c in range(1, cols):
      reached += scan(0, c, 1, 1)
    # print("Down right", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

    reached = 0
    for r in range(rows):
      reached += scan(r, cols - 1, 1, -1)
    for c in range(cols - 1):
      reached += scan(0, c, 1, -1)
    # print("Down left", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

    reached = 0
    for r in range(rows):
      reached += scan(r, cols - 1, 0, -1)
    # print("Left", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

    reached = 0
    for r in range(rows):
      reached += scan(r, cols - 1, -1, -1)
    for c in range(cols - 1):
      reached += scan(rows - 1, c, -1, -1)
    # print("Top left", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

    reached = 0
    for r in range(rows):
      reached += scan(r, 0, -1, 1)
    for c in range(1, cols):
      reached += scan(rows - 1, c, -1, 1)
    # print("Top right", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

    reached = 0
    for r in range(rows):
      reached += scan(r, 0, 0, 1)
    # print("Right", reached)
    reached_total += reached
    warriors += check_warriors()
    if warriors >= 100000: break

  print("Part 2", reached_total)


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()