import itertools
from sys import stdin


class Byte:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.corrupted = False
        self.distance = 9999

    def __hash__(self):
        return hash((self.x, self.y))


class MemorySpace:

    def __init__(self):
        self.bytes = [[Byte(x, y) for x in range(71)] for y in range(71)]

    def byte(self, x: int, y: int):
        if not 0 <= x < 71:
            return None
        if not 0 <= y < 71:
            return None
        return self.bytes[y][x]

    def all_bytes(self):
        return itertools.chain(*self.bytes)

    def start(self):
        return self.byte(0, 0)

    def end(self):
        return self.byte(70, 70)

    def neighbours(self, byte: Byte):
        return (
            neighbour
            for neighbour in [
                self.byte(byte.x, byte.y - 1),
                self.byte(byte.x, byte.y + 1),
                self.byte(byte.x - 1, byte.y),
                self.byte(byte.x + 1, byte.y),
            ]
            if neighbour is not None
        )

    def corrupt(self, x: int, y: int):
        byte = self.byte(x, y)
        if byte is None:
            return
        byte.corrupted = True

    def calculate_distances(self):
        for byte in self.all_bytes():
            byte.distance = 9999
        end = self.end()
        end.distance = 0
        search_frontier = {end}
        while search_frontier:
            this = search_frontier.pop()
            for neighbour in self.neighbours(this):
                if neighbour.corrupted:
                    continue
                if neighbour.distance <= this.distance + 1:
                    continue
                neighbour.distance = this.distance + 1
                search_frontier.add(neighbour)


memory_space = MemorySpace()
for byte in stdin.read().splitlines():
    x, y = map(int, byte.split(","))
    memory_space.corrupt(x, y)
    memory_space.calculate_distances()
    if memory_space.start().distance < 9999:
        continue
    print(x, y)
    break
