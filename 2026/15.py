#!/bin/env python3


def _read(file: str) -> str:
  with open(file, "r") as handle:
    return handle.readline().strip()
  assert False

def part1():
  pieces: list[str] = list(_read("15-part1.txt"))
  flips: int = 0
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
  print("Part 1", flips, sep="\t")

  
def main():
  part1()
  # part2()
  # part3()


if __name__ == "__main__":
  main()