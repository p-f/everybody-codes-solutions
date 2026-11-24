#!/bin/env python3


def _read(file: str) -> str:
  with open(file, "r") as handle:
    return handle.readline().strip()
  assert False

def _sort_using_flips(pieces: list[str]) -> tuple[int, int]:
  flips: int = 0
  flipped: int = 0
  left: int = 0
  def _end(target: str, left_pos: int) -> int | None:
    for pos in range(len(pieces) - 1, left_pos, -1):
      if pieces[pos] == target:
        return pos
    return None
  while left < len(pieces):
    # Advance to end of current group
    while left < len(pieces) - 1 and pieces[left + 1] == pieces[left]:
      left += 1
    # Find other group
    next_end = _end(pieces[left], left)
    if not next_end:
      left += 1
      continue
    # Flip
    pieces[left + 1:next_end + 1] = pieces[left + 1:next_end + 1][::-1]
    left += 1
    flips += 1
    flipped += next_end - left + 1
    # print("Progress", left / len(pieces) * 100)
  return flips, flipped

def part1():
  pieces: list[str] = list(_read("16-part1.txt"))
  flips, _ = _sort_using_flips(pieces)
  print("Part 1", flips, sep="\t")

def part2():
  pieces: list[str] = list(_read("16-part2.txt")) * 10
  _, flipped = _sort_using_flips(pieces)
  print("Part 2", flipped, sep="\t")

def _sort_by_picking(pieces: list[str]) -> int:
  left: int = 0
  right: int = len(pieces) - 1
  flips: int = 0
  extra: list[str] = []
  current: str = pieces[left]
  while left <= right:
    # Go to end of left group
    while left <= right and pieces[left] == current: left += 1
    # Find group on the right
    while right >= left and (pr := pieces[right]) != current:
      extra.append(pr)
      right -= 1
    flips += right - left + 1
    # Now flipped, go the end of next group (now from end)
    while right >= left and pieces[right] == current: right -= 1
    # Find group on the left
    while left <= right and (pl := pieces[left]) != current:
      extra.append(pl)
      left += 1
    flips += right - left + 1
  # Remaining characters will exclude current one -> will terminate when all are picked
  if extra: flips += _sort_by_picking(extra)
  return flips

def part3():
  pieces: list[str] = list(_read("16-part3.txt")) * 100
  flipped = _sort_by_picking(pieces)
  print("Part 2", flipped, sep="\t")


def main():
  part1()
  part2()
  part3()

if __name__ == "__main__":
  main()