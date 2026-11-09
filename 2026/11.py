#!/bin/env python3


from collections import defaultdict
from itertools import pairwise

type Graph = dict[int, set[int]]

def _read(path: str) -> Graph:
  graph: Graph = defaultdict(set)
  with open(path, "r") as h:
    portals: int = int(h.readline().strip().split()[1])
    for i, j in pairwise(range(1, portals + 1)):
      graph[i].add(j)
      graph[j].add(i)
    graph[portals].add(1)
    graph[1].add(portals)
    h.readline()
    while l := h.readline():
      s, d = l.strip().split()
      s = int(s)
      d = int(d)
      graph[s].add(d)
      graph[d].add(s)
  return graph

def part1():
  g: Graph = _read("11-part1.txt")
  nodes: int = len(g)
  res: int = 0
  for start in g:
    dist = [-1] * nodes
    dist[start - 1] = 0
    queue = [start]
    while queue:
      head = queue.pop(0)
      head_dist = dist[head - 1]
      for neigh in g[head]:
        if dist[neigh - 1] == -1:
          dist[neigh - 1] = head_dist + 1
          queue.append(neigh)
    res += sum(dist)
  res_orig: int = (nodes // 2) ** 2 * nodes
  print("Part 1", res_orig - res)



def main():
  part1()
  # part2()
  # part3()


if __name__ == "__main__":
  main()