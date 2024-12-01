from sys import stdin


aa = []
bb = [0] * 100_000

for row in stdin.readlines():
    a, b = map(int, row.split())
    aa.append(a)
    bb[b] += 1

similarity = 0

for a in aa:
    similarity += a * bb[a]

print(similarity)
