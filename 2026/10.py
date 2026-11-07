#!/bin/env python3

from dataclasses import dataclass
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

@dataclass
class GhostData:
  id: int
  r: int
  c: int
  dr: int
  dc: int
  life: int = 1000000000000

  def rotate(self) -> None:
    match (self.dr, self.dc):
      case (0, 1):
        self.dr, self.dc = (1, 0)
      case(1, 0):
        self.dr, self.dc = (0, -1)
      case (0, -1):
        self.dr, self.dc = (-1, 0)
      case (-1, 0):
        self.dr, self.dc = (0, 1)
      case _:
        raise RuntimeError()
    self.life -= 1

  def pos(self) -> tuple[int, int]:
    return self.r, self.c

  def posandid(self) -> tuple[int, int, int]:
    return self.r, self.c, self.id

  def next_pos(self) -> tuple[int, int]:
    return self.r + self.dr, self.c + self.dc

  def advance(self) -> None:
    self.r += self.dr
    self.c += self.dc

  def turn180(self) -> None:
    self.dr = -self.dr
    self.dc = -self.dc
    self.life -= 1

type GhostPosPart = tuple[int, int, int, int, int]
type GhostLivesState = tuple[int, ...]
type GhostsPosState = tuple[GhostPosPart, ...]
def _encode_state(ghosts: list[GhostData], round: int) -> tuple[GhostsPosState, int, GhostLivesState]:
  return tuple(
      (g.id, g.r, g.c, g.dr, g.dc,) for g in ghosts
    ), round,  \
    tuple(
      (g.life) for g in ghosts
    )

def part3():
  field: list[str] = _read("10-part3.txt")
  ghosts: list[GhostData] = []
  for i, (r, d, dr, dc) in enumerate(_find_ghosts(field)):
    ghosts.append(GhostData(i, r, d, dr, dc))
  prev_states: dict[GhostsPosState, tuple[int, GhostLivesState]] = {}
  round = 0
  while ghosts:
    round += 1
    for g in ghosts:
      r, c = g.next_pos()
      if field[r][c] == '#':
        g.rotate()
      else:
        g.advance()
    if any(g.life == 0 for g in ghosts):
      ghosts = sorted((g for g in ghosts if g.life > 0), key=GhostData.posandid)
      # print("Die at", round, "now", len(ghosts))
    else:
      ghosts.sort(key=GhostData.posandid)
    num_ghosts: int = len(ghosts)
    if num_ghosts > 1:
      for i in range(num_ghosts):
        gpos = ghosts[i].pos()
        if gpos == ghosts[(i + 1) % num_ghosts].pos() or gpos == ghosts[(i + num_ghosts - 1) % num_ghosts].pos():
          ghosts[i].turn180()
    if any(g.life == 0 for g in ghosts):
      ghosts = [g for g in ghosts if g.life]
      # print("Die at ", round, "now: ", len(ghosts))
    num_ghosts = len(ghosts)
    gk, round, glives = _encode_state(ghosts, round)
    if gk in prev_states:
      prev_round, prev_lives = prev_states[gk]
      # print("Found previous state: ")
      # print(prev_round, prev_lives)
      # print("Current")
      # print(round, glives)
      # for gi in range(num_ghosts):
      #   print(prev_lives[gi], "vs", glives[gi], "Delta:", prev_lives[gi] - glives[gi], "Skips", glives[gi] // (prev_lives[gi] - glives[gi]))
      skips = min(glives[gi] // (prev_lives[gi] - glives[gi]) - 1 for gi in range(num_ghosts))
      skip_rounds = skips * (round - prev_round)
      if skip_rounds <= 1:
        prev_states[gk] = round, glives
      else:
        # print("Skipping", skip_rounds)
        round += skip_rounds
        for gi in range(num_ghosts):
          # print("old", ghosts[gi])
          ghosts[gi].life -= skips * (prev_lives[gi] - glives[gi])
          # print("new", ghosts[gi])
    else:
      prev_states[gk] = round, glives
    if any(g.life == 0 for g in ghosts):
      ghosts = [g for g in ghosts if g.life]
      prev_states.clear()
      # print("Die at round", round, "now", len(ghosts))
    # if round % 1000000 == 0: print("Round", round, "Ghosts", len(ghosts), ghosts)
  print("Part 2", round)


def main():
  part1()
  part2()
  part3()


if __name__ == "__main__":
  main()