#!/bin/env python3

from functools import cmp_to_key
from itertools import product

def _read_input(name: str):
  with open(name, "r") as handle:
    while r := handle.readline():
      yield r.strip()

def main():
  # Part 1
  res = 0
  for line in _read_input("02-part1.txt"):
    alloys = set()
    cmps = set()
    def _cmp(pri, sec):
      if (pri, sec) in cmps:
        return -1
      else:
        return 1
    for part in line.split(" "):
      l = int(part[0])
      ge = part[1] == '>'
      r = int(part[2])
      alloys.add(l)
      alloys.add(r)
      if ge:
        cmps.add((l, r))
      else:
        cmps.add((r, l))
    chksum = 0
    for digit in sorted(alloys, key=cmp_to_key(_cmp)):
      chksum *= 10
      chksum += digit
    res += chksum
  print("Part 1", res, sep="\t")
  # Part 2
  res = 0
  for line in _read_input("02-part2.txt"):
    alloys = set()
    cmps = {}
    def _cmp(pri, sec):
      if (pri, sec) in cmps: return cmps[(pri, sec)]
      for mid in alloys:
        if mid != pri and mid != sec:
          c1 = _cmp(pri, mid)
          c2 = _cmp(mid, sec)
          if c1 == c2:
            return c1
      raise ValueError()
    for part in line.split(" "):
      l = int(part[0])
      ge = part[1] == '>'
      r = int(part[2])
      alloys.add(l)
      alloys.add(r)
      if ge:
        cmps[(l, r)] = -1
        cmps[(r, l)] = 1
      else:
        cmps[(l, r)] = 1
        cmps[(r, l)] = -1
    chksum = 0
    for digit in sorted(alloys, key=cmp_to_key(_cmp)):
      chksum *= 10
      chksum += digit
    res += chksum
  print("Part 2:", res, sep="\t")
  # Part 3
  res = 0
  for line in _read_input("02-part3.txt"):
    alloys = set()
    cmps = {}
    for part in line.split(" "):
      l = int(part[0])
      ge = part[1] == '>'
      r = int(part[2])
      alloys.add(l)
      alloys.add(r)
      if ge:
        cmps[(l, r)] = -1
        cmps[(r, l)] = 1
      else:
        cmps[(l, r)] = 1
        cmps[(r, l)] = -1
    # Create transitive hull
    updated = True
    while updated:
      updated = False
      for pair1, pair2 in product(cmps, cmps):
        if pair1 == pair2 or cmps[pair1] != cmps[pair2] or pair1[1] != pair2[0]:
          continue
        new_pair = pair1[0], pair2[1],
        if new_pair not in cmps:
          updated = True
          cmp_res = cmps[pair1]
          cmps[new_pair] = cmp_res
          cmps[(pair2[1], pair1[0])] = -cmp_res
    chksum = 0
    for digit in sorted(alloys, key=cmp_to_key(lambda l, r: cmps[(l, r)])):
      chksum *= 10
      chksum += digit
    res += chksum
  print("Part 3:", res, sep="\t")
    
    




if __name__ == "__main__":
  main()