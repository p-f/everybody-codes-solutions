#!/bin/env python3

def _read(path: str):
  with open(path, "r") as handle:
    while l:= handle.readline():
      yield l.strip()

def part1():
  field: list[str] = list(_read("05-part1.txt"))
  rows = len(field)
  cols = len(field[0])
  r = rows // 2
  c = cols // 2
  queue = [(r, c)]
  land = [[False] * cols for _ in range(rows)]
  land[r][c] = True
  landsize = 1
  def _neigh(rr: int, cc: int):
    for dr in (-1, 0, 1):
      for dc in (-1, 0, 1):
        if dr == 0 and dc == 0: continue
        rn = rr + dr
        if rn < 0 or rn >= rows: continue
        cn = cc + dc
        if cn < 0 or cn >= cols: continue
        yield (rn, cn)
  def canbe(rcenter, ccenter):
    num = 0
    for (rn, cn) in _neigh(rcenter, ccenter):
      if land[rn][cn] or field[rn][cn] == '1':
        num += 1
    return num >= 5
  while queue:
    for (r, c) in _neigh(*queue.pop(0)):
      if not land[r][c] and canbe(r, c):
        land[r][c] = True
        landsize += 1
        queue.append((r, c))
  print("Part 1:", landsize)

def part2():
  _read("05-part2.txt")
  res = 0
  print("Part 2:", res)

def part3():
  _read("05-part3.txt")
  res = 0
  print("Part 3:", res)


def main():
  part1()
  part2()
  part3()


if __name__ == "__main__":
  main()