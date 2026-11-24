#!/bin/env python3

from enum import Enum

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
  grid: Grid = _read("17-part1.txt")
  dist: list[list[int]] = _get_dists(grid)
  print("Part 1:", dist[-1][-1])

def part2():
  grid: Grid = _read("17-part2.txt")
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

class Dir(Enum):
  LEFT = (0, -1)
  RIGTH = (0, 1)
  TOP = (-1, 0)
  BOTTOM = (1, 0)

type PosAndDir = tuple[int, int, Dir]

def _walk(grid: Grid, start: PosAndDir, before: PosAndDir) -> int:
  max_row: int = len(grid) - 1
  max_col: int = len(grid[0]) - 1
  curr, prev = start, before
  def _is_goal(p: PosAndDir) -> bool:
    return p[0] == max_row and p[1] == max_col and p[2] in (Dir.BOTTOM, Dir.RIGTH,)
  def _free(rr: int, cc: int) -> bool:
    return rr < 0 or rr > max_row or cc < 0 or cc > max_col or grid[rr][cc] == '.'
  def _can_move(rn: int, cn: int, dir: Dir) -> bool:
    if not (0 <= rn <= max_row and 0 <= cn <= max_col and grid[rn][cn] == '#'):
      return False
    # Side must be free
    rd, cd = dir.value
    return _free(rn + rd, cn + cd)
  def _valid_move(old: PosAndDir, new: PosAndDir) -> bool:
    # If they are on the same row or column we are good, other checks will
    # prevent illegal moves
    if old[0] == new[0] or old[1] == new[1]: return True
    # They must be diagonal, check if they are connected
    # Just check if the square (height 2, width 1) has exactly one free space
    free_count: int = 0
    for rr in (old[0], new[0],):
      for cc in (old[1], new[1],):
        if _free(rr, cc): free_count += 1
    return free_count == 1
  units: int = 1
  seen: set[PosAndDir] = {curr}
  while not _is_goal(curr):
    units += 1
    r, c, d = curr
    next_pos: list[PosAndDir] = []
    match d:
      case Dir.LEFT:
        next_pos += (
          (r - 1, c, d,), (r + 1, c, d,), (r, c, Dir.TOP,), (r, c, Dir.BOTTOM,),
          (r - 1, c - 1, Dir.BOTTOM), (r + 1, c - 1, Dir.TOP)
        )
      case Dir.RIGTH:
        next_pos += (
          (r - 1, c, d,), (r + 1, c, d,), (r, c, Dir.TOP,), (r, c, Dir.BOTTOM,),
          (r - 1, c + 1, Dir.BOTTOM), (r + 1, c + 1, Dir.TOP),
        )
      case Dir.TOP:
        next_pos += (
          (r, c - 1, d,), (r, c + 1, d,), (r, c, Dir.LEFT,), (r, c, Dir.RIGTH,),
          (r - 1, c - 1, Dir.RIGTH,), (r - 1, c + 1, Dir.LEFT,),
        )
      case Dir.BOTTOM:
        next_pos += (
          (r, c - 1, d,), (r, c + 1, d,), (r, c, Dir.LEFT,), (r, c, Dir.RIGTH,),
          (r + 1, c - 1, Dir.RIGTH,), (r + 1, c + 1, Dir.LEFT,),
        )
      case _: raise ValueError(curr)
    next: PosAndDir | None = None
    for candidate in next_pos:
      if candidate != prev and candidate not in seen and _can_move(*candidate) and _valid_move(curr, candidate):
        next = candidate
        break
    assert next, f"Not sure where to go from {curr}"
    seen.add(curr)
    prev, curr = curr, next
  return units

def part3():
  grid: Grid = _read("17-part3.txt")
  res: int = min(
    _walk(grid, (0, 0, Dir.TOP,), (0, 0, Dir.LEFT,)),
    _walk(grid, (0, 0, Dir.LEFT,), (0, 0, Dir.TOP,)))
  print("Part 3:", res, sep="\t")  


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()