from sys import stdin


aa = []
bb = []

for row in stdin.readlines():
    a, b = map(int, row.split())
    aa.append(a)
    bb.append(b)

aa.sort()
bb.sort()

print(sum(abs(a - b) for a, b in zip(aa, bb)))
