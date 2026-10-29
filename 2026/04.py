#!/bin/env python3

from collections import Counter
from itertools import count

def _read(path: str):
  with open(path, "r") as handle:
    while l:= handle.readline():
      yield map(int, map(lambda p: p.split("=")[1], l.split()))

def part1():
  per_participant: dict[int, int] = Counter()
  for id, _, _, time in _read("04-part1.txt"):
    per_participant[id] += time
  res = 0
  for i, t in enumerate(sorted(per_participant.values())):
    res += (i + 1) * t
  print("Part 1:", res)

def part2():
  per_participant: dict[int, int] = Counter()
  num_participations: dict[int, int] = Counter()
  for id, _, _, time in _read("04-part2.txt"):
    per_participant[id] += time
    num_participations[id] += 1
  res = 0
  part_and_time = [(-num_participations[id], per_participant[id]) for id in per_participant.keys()]
  part_and_time.sort()
  for i, (_, t) in enumerate(part_and_time):
    res += (i + 1) * t
  print("Part 2:", res)

def part3():
  data = list(tuple(t) for t in _read("04-part3.txt"))
  quests = set(d[1] for d in data)
  scores = Counter()
  for q in quests:
    times: dict[int, int] = Counter()
    for part in (1, 2, 3):
      participate = set()
      for id, quest, dpart, time in data:
        if quest != q or part != dpart:
          continue
        participate.add(id)
        times[id] += time
      if not participate: continue
      f_data = [(time, id) for (id, time) in times.items() if id in participate]
      f_data.sort()
      # print(q, part, f_data)
      score = 50 * part
      last_time = f_data[0][0]
      with_time = 0
      for time, id in f_data:
        if time > last_time:
          score -= with_time
          with_time = 1
          last_time = time
        else:
          with_time += 1
        if score <= 0: break
        scores[id] += score
        # print("Q", q, "P", part, "E", id, "t", time, "score", score)
  max_scores = sorted(scores.values(), reverse=True)
  res = 0
  prev_score = max_scores[0]
  rank = 1
  with_rank = 0
  for s in max_scores:
    if s == prev_score:
      with_rank += 1
    else:
      rank += with_rank
      with_rank = 1
      prev_score = s
    res += (rank) * s
  print("Part 3", res)


def main():
  part1()
  part2()
  part3()


if __name__ == "__main__":
  main()