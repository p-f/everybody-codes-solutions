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

def part3():
  f: Field = _read("12-part3.txt")
  rows: int = len(f)
  cols: int = len(f[0])
  def _size(r: int, c: int) -> int:
    points: set[tuple[int, int]] = set()
    queue = [(r, c)]
    f[r][c] = '/'
    while queue:
      r, c = queue.pop(0)
      points.add((r, c,))
      for (rn, cn) in ((r + 1, c,), (r - 1, c,), (r, c + 1,), (r, c- 1,)):
        if 0 <= rn < rows and 0 <= cn < cols and f[rn][cn] == '#':
          queue.append((rn, cn,))
          f[rn][cn] = '/'
    r_min = min(p[0] for p in points)
    r_max = max(p[0] for p in points)
    c_min = min(p[1] for p in points)
    c_max = max(p[1] for p in points)
    top_width = len([p for p in points if p[0] == r_min])
    bottom_width = len([p for p in points if p[0] == r_max])
    left_height = len([p for p in points if p[1] == c_min])
    right_height = len([p for p in points if p[1] == c_max])
    if left_height == right_height or top_width == bottom_width:
      # Is it a square?
      if len(points) == (left_height * top_width):
        return min(left_height, top_width) # its a square
      # There must be an empty part
      # Find the first and last . inside the shape
      empty_row_start: int | None = None
      empty_col_start: int | None = None
      empty_row_end: int | None = None
      empty_col_end: int | None = None
      for rr in range(r_min, r_max + 1):
        for cc in range(c_min, c_max + 1):
          if f[rr][cc] == '.':
            if empty_row_start is None:
              empty_row_start = rr
              empty_col_start = cc
            empty_row_end = rr
            empty_col_end = cc
      assert empty_col_start and empty_col_end and empty_row_start and empty_row_end
      # Calculate bar widths
      top: int = empty_row_start - r_min
      bottom: int = r_max - empty_row_end
      left: int  = empty_col_start - c_min
      right: int = c_max - empty_col_end
      # print("Bounds", r_min, r_max, c_min, c_max)
      # print("Empty", empty_row_start, empty_row_end, empty_col_start, empty_col_end)
      # print("Shape", top, bottom, left, right)
      cost: int = top + bottom + left + right # Just slice the sides as bars, based on their width
      # Can also try separating the left and right bars
      cost_lr_first: int = left + right
      # Now we have 2 blocks in top and bottom left
      top_block_after_lr: tuple[int, int] = top, empty_col_end - empty_col_start + 1
      bottom_block_after_lr: tuple[int, int] = bottom, empty_col_end - empty_col_start + 1
      cost_lr_first += min(*top_block_after_lr) + min(*bottom_block_after_lr)
      cost = min(cost, cost_lr_first)
      # Can also try separating top and bottom first
      cost_tb_first: int = top + bottom
      # Now we have 2 blocks left and right
      left_block_after_tb: tuple[int, int] = left, empty_row_end - empty_row_start + 1
      right_block_after_tb: tuple[int, int] = right, empty_row_end - empty_row_start + 1
      cost_tb_first += min(*left_block_after_tb) + min(*right_block_after_tb)
      cost = min(cost, cost_tb_first)
      # print("Outer shape cost", cost)
      # There could be something on the inside
      for ri in range(empty_row_start, empty_row_end):
        for ci in range(empty_col_start, empty_col_start):
          if f[ri][ci] == '#':
            c = _size(ri, ci)
            # print("Inner shape at", ri, ci, "with", c)
            cost += c
      return cost
    # Otherwise its just an L
    size1 = min(left_height, right_height)
    size2 = min(top_width, bottom_width)
    return min(size1 + size2, max(top_width, bottom_width), max(left_height, right_height))    
  res: int = 0
  for r in range(rows):
    for c in range(cols):
      if f[r][c] == '#':
        size = _size(r, c)
        res += size
  print("Part 3", res)

def main():
  part1()
  part2()
  part3()


if __name__ == "__main__":
  main()