#!/bin/env python3

type Grid = list[str]

def _read(file: str) -> Grid:
  lines: Grid = []
  with open(file, "r") as handle:
    while l := handle.readline():
      lines.append(l.strip())
  return lines

_UNSEEN: int = 999999999

def _get_dists(grid: Grid) -> list[list[int]]:
  rows: int = len(grid)
  cols: int = len(grid[0])
  dist: list[list[int]] = [[_UNSEEN] * cols for _ in range(rows)]
  dist[0][0] = 0
  queue: list[tuple[int, int]] = [(0, 0)]
  def _try_move(rn: int, cn: int, new_dist: int):
    if 0 <= rn < rows and 0 <= cn < cols and grid[rn][cn] == '#' and new_dist < dist[rn][cn]:
      queue.append((rn, cn,))
      dist[rn][cn] = new_dist
  while queue:
    r, c = queue.pop(0)
    neigh_dist = dist[r][c] + 1
    _try_move(r + 1, c, neigh_dist)
    _try_move(r - 1, c, neigh_dist)
    _try_move(r, c + 1, neigh_dist)
    _try_move(r, c - 1, neigh_dist)
  return dist

def part1():
  grid: Grid = _read("16-part1.txt")
  dist: list[list[int]] = _get_dists(grid)
  print("Part 1:", dist[-1][-1])

def part2():
  grid: Grid = _read("16-part2.txt")
  dist: list[list[int]] = _get_dists(grid)
  rows: int = len(grid)
  cols: int = len(grid[0])
  borders: int = 0
  for r in range(rows):
    for c in range(cols):
      if dist[r][c] == _UNSEEN: continue
      if r == 0 or dist[r - 1][c] == _UNSEEN: borders += 1
      if r == rows - 1 or dist[r + 1][c] == _UNSEEN: borders += 1
      if c == 0 or dist[r][c - 1] == _UNSEEN: borders += 1
      if c == cols - 1 or dist[r][c + 1] == _UNSEEN: borders += 1
  print("Part 2:", borders, sep="\t")

  
def main():
  part1()
  part2()
  # part3()

if __name__ == "__main__":
  main()