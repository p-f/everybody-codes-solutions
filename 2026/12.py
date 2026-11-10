#!/bin/env python3

type Field = list[list[str]]

def _read(path: str) -> Field:
  f: Field = []
  with open(path, "r") as h:
    while l := h.readline():
      f.append(list(l.strip()))
  return f

def part1():
  f: Field = _read("12-part1.txt")
  rows: int = len(f)
  cols: int = len(f[0])
  res: int = 0
  def _shape_size(r_top: int, c_top: int) -> tuple[int, int]:
    r: int = r_top
    while r < rows and f[r][c_top] == '#': r += 1
    c: int = c_top
    while c < cols and f[r_top][c] == '#': c += 1
    return r - r_top, c - c_top
  for r in range(rows):
    for c in range(cols):
      if f[r][c] == '#' and (r == 0 or f[r - 1][c] == '.') and (c == 0 or f[r][c - 1] == '.'):
        res += min(*_shape_size(r, c))
  print("Part 1", res)

def part2():
  f: Field = _read("12-part2.txt")
  rows: int = len(f)
  cols: int = len(f[0])
  def _shape_size(r: int, c: int) -> int:
    points: set[tuple[int, int]] = set()
    queue = [(r, c)]
    f[r][c] = '.'
    while queue:
      r, c = queue.pop(0)
      points.add((r, c,))
      for (rn, cn) in ((r + 1, c,), (r - 1, c,), (r, c + 1,), (r, c- 1,)):
        if 0 <= rn < rows and 0 <= cn < cols and f[rn][cn] == '#':
          queue.append((rn, cn,))
          f[rn][cn] = '.'
    r_min = min(p[0] for p in points)
    r_max = max(p[0] for p in points)
    c_min = min(p[1] for p in points)
    c_max = max(p[1] for p in points)
    top_width = len([p for p in points if p[0] == r_min])
    bottom_width = len([p for p in points if p[0] == r_max])
    left_height = len([p for p in points if p[1] == c_min])
    right_height = len([p for p in points if p[1] == c_max])
    if left_height == right_height or top_width == bottom_width:
      return min(left_height, top_width) # its a square
    size1 = min(left_height, right_height)
    size2 = min(top_width, bottom_width)
    return min(size1 + size2, max(top_width, bottom_width), max(left_height, right_height))  
  res: int = 0
  for r in range(rows):
    for c in range(cols):
      if f[r][c] == '#':
        size = _shape_size(r, c)
        res += size
  print("Part 2", res)


def main():
  part1()
  part2()
  # part3()


if __name__ == "__main__":
  main()