from sys import stdin

from grid import Grid, GridTile


class Byte(GridTile):

    def __init__(self, u: int, v: int):
        super().__init__(u, v)
        self.corrupted = False
        self.distance = 9999

    def display(self):
        if self.corrupted:
            return "#"
        else:
            return "."


class Memory(Grid[Byte]):

    def __init__(self, height: int, width: int):
        super().__init__(
            [[Byte(u, v) for v in range(width)] for u in range(height)]
        )

    def start(self):
        return self.tile(0, 0)

    def end(self):
        return self.tile(self.height - 1, self.width - 1)

    def corrupt(self, u: int, v: int):
        byte = self.tile(u, v)
        if byte is None:
            return
        byte.corrupted = True

    def calculate_distances(self):
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


memory = Memory(71, 71)
for byte in stdin.read().splitlines()[:1024]:
    x, y = map(int, byte.split(","))
    memory.corrupt(y, x)
memory.calculate_distances()
print(memory.start().distance)
