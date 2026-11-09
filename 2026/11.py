#!/bin/env python3


from collections import defaultdict
from itertools import pairwise, product

type Graph = dict[int, set[int]]

def _read1(path: str) -> Graph:
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

def _read2(path: str) -> tuple[Graph, list[tuple[int, int]]]:
  graph: Graph = defaultdict(set)
  short: list[tuple[int, int]] = []
  with open(path, "r") as h:
    portals: int = int(h.readline().strip().split()[1])
    for i in range(portals):
      for d in range(-3, 4):
        if d == 0: continue
        j = (i + portals + d) % portals
        graph[i].add(j)
        graph[j].add(i)
    h.readline()
    while l := h.readline():
      s, d = l.strip().split()
      short.append((int(s) - 1, int(d) - 1, ))
  return graph, short

def part1():
  g: Graph = _read1("11-part1.txt")
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

def _agg_dists(g: Graph) -> int:
  nodes: int = len(g)
  res: int = 0
  nodes: int
  for start in g:
    dist = [-1] * nodes
    dist[start] = 0
    queue = [start]
    while queue:
      head = queue.pop(0)
      head_dist = dist[head]
      for neigh in g[head]:
        if dist[neigh] == -1:
          dist[neigh] = head_dist + 1
          queue.append(neigh)
    res += sum(dist)
  return res

def part2():
  graph: Graph
  short: list[tuple[int, int]]
  graph, short = _read2("11-part2.txt")
  res_orig = _agg_dists(graph)
  for s, d in short:
    graph[s].add(d)
    graph[d].add(s)
  min_res = _agg_dists(graph)
  for ss, dd in product(graph, graph):
    if ss == dd or dd in graph[ss]:
      continue
    graph[ss].add(dd)
    graph[dd].add(ss)
    min_res = min(min_res, _agg_dists(graph))
    graph[dd].remove(ss)
    graph[ss].remove(dd)
  print("Part 2:", res_orig - min_res)


def main():
  part1()
  part2()
  # part3()


if __name__ == "__main__":
  main()