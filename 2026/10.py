#!/bin/env python3

from itertools import groupby

def _read(path: str) -> list[str]:
  rules: list[str] = []
  with open(path, "r") as h:
    while l := h.readline():
      rules.append(l.strip())
  return rules

type Ghost = tuple[int, int, int, int]

DIR = {
  '>': (0, 1),
  'v': (1, 0),
  '<': (0, -1),
  '^': (-1, 0)
}

DIR_DELTAS = list(DIR.values())

def _rotate(d: tuple[int, int]) -> tuple[int, int]:
  for i, exp in enumerate(DIR_DELTAS):
    if exp == d:
      return DIR_DELTAS[(i + 1) % 4]
  raise ValueError(d)

def _find_ghosts(field: list[str]) -> list[Ghost]:
  g: list[Ghost] = []
  for r, r_data in enumerate(field):
    for c, cell in enumerate(r_data):
      if cell in DIR:
        g.append((r, c) + DIR[cell])
  return g

def part1():
  field: list[str] = _read("10-part2.txt")
  ghosts: list[Ghost] = _find_ghosts(field)
  collision: int = 0
  for step in range(10):
    for i, (r, c, dr, dc) in enumerate(ghosts):
      if field[r + dr][c + dc] == '#':
        ghosts[i] = (r, c) + _rotate((dr, dc))
        collision += 1
      else:
        ghosts[i] = (r + dr, c + dc, dr, dc)
    ghosts.sort()
    for _, samepos in groupby(range(len(ghosts)), key=lambda i: (ghosts[i][0], ghosts[i][1])):
      samepos = list(samepos)
      if len(samepos) == 1: continue
      for gi in samepos:
        r, c, dr, dc = ghosts[gi]
        ghosts[gi] = (r, c, -dr, -dc)
        collision += 1
  print("Part 1", collision)

type GhostWithLife = tuple[int, int, int, int, int]

def part2():
  field: list[str] = _read("10-part2.txt")
  ghosts: list[GhostWithLife] = [g + (10000,) for g in _find_ghosts(field)]
  round = 0
  while ghosts:
    round += 1
    for i, (r, c, dr, dc, life) in enumerate(ghosts):
      if field[r + dr][c + dc] == '#':
        ghosts[i] = (r, c) + _rotate((dr, dc)) + (life - 1,)
      else:
        ghosts[i] = (r + dr, c + dc, dr, dc, life)
    ghosts = sorted(g for g in ghosts if g[4])
    for _, samepos in groupby(range(len(ghosts)), key=lambda i: (ghosts[i][0], ghosts[i][1])):
      samepos = list(samepos)
      if len(samepos) == 1: continue
      for gi in samepos:
        r, c, dr, dc, life = ghosts[gi]
        ghosts[gi] = (r, c, -dr, -dc, life - 1)
    ghosts = [g for g in ghosts if g[4]]
    # print("Round", round, "Ghosts", len(ghosts), ghosts)
  print("Part 2", round)



def main():
  part1()
  part2()


if __name__ == "__main__":
  main()