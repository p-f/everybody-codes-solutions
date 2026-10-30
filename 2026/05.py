#!/bin/env python3

def _read(path: str):
  with open(path, "r") as handle:
    while l:= handle.readline():
      yield l.strip()

def part123():
  field: list[str] = list(_read("05-part1.txt"))
  rows = len(field)
  cols = len(field[0])
  r = rows // 2
  c = cols // 2
  queue = [(r, c)]
  land = [[0] * cols for _ in range(rows)]
  land[r][c] = 1
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
        land[r][c] = 1
        landsize += 1
        queue.append((r, c))
  print("Part 1:", landsize)
  sandsize = 0
  for r in range(rows):
    for c in range(cols):
      if not land[r][c]: continue
      if r == 0 or c == 0 or r == rows - 1 or c == cols - 1:
        sandsize += 1
        queue.append((r, c))
        land[r][c] = 2
        continue
      has_sea = False
      for (rn, cn) in _neigh(r, c):
        if not land[rn][cn]:
          has_sea = True
          break
      if has_sea:
        sandsize += 1
        queue.append((r, c))
        land[r][c] = 2
  def canbesand(rcenter, ccenter):
    num = 0
    for (rn, cn) in _neigh(rcenter, ccenter):
      if land[rn][cn] == 2:
        num += 1
    return num >= 5
  while queue:
    for (r, c) in _neigh(*queue.pop(0)):
      if land[r][c] == 1 and canbesand(r, c):
        land[r][c] = 2
        sandsize += 1
        queue.append((r, c))
  print("Part 2:", sandsize)
  treesize = 0
  for r in range(2, rows - 2):
    for c in range(2, cols - 2):
      if land[r][c] != 1: continue
      landcount = 0
      for rt in range(r - 2, r + 3):
        for ct in range(c - 2, c + 3):
          if (land[rt][ct] == 1 or land[rt][ct] == 3) and not (abs(rt - r) == 2 and abs(ct - c) == 2):
            landcount += 1
      if landcount == 21:
        land[r][c] = 3
        treesize += 1
  # print(treesize)
  # for l in land:
  #   print(*l, sep="")
  for _ in (1, 2):
    for r in range(1, rows - 1):
      for c in range(1, cols - 1):
        if land[r][c] != 1: continue
        treecount = 0
        for (rn, cn) in _neigh(r, c):
          if land[rn][cn] == 3:
            treecount += 1
          elif land[rn][cn] == 2:
            treecount = 0
            break
        if treecount >= 4:
          land[r][c] = 4 # tmp
          treesize += 1
    for r in range(rows):
      for c in range(cols):
        if land[r][c] == 4:
          land[r][c] = 3
    # print(treesize)
    # for l in land:
    #   print(*l, sep="")
  print("Part 3:", treesize)


def main():
  part123()


if __name__ == "__main__":
  main()