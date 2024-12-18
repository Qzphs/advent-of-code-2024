from sys import stdin

from grid import Grid, Tile


class Byte(Tile):

    def __init__(self, u: int, v: int):
        super().__init__(u, v)
        self.corrupted = False
        self.distance = 9999

    def display(self):
        if self.corrupted:
            return "#"
        else:
            return "."


class Memory(Grid):

    def __init__(self, height: int, width: int):
        super().__init__(
            [[Byte(u, v) for v in range(width)] for u in range(height)]
        )

    def start(self) -> Byte:
        return self.tile(0, 0)

    def end(self) -> Byte:
        return self.tile(self.height - 1, self.width - 1)

    def corrupt(self, u: int, v: int):
        byte = self.tile(u, v)
        if byte is None:
            return
        assert isinstance(byte, Byte)
        byte.corrupted = True

    def calculate_distances(self):
        end = self.end()
        end.distance = 0
        search_frontier = {end}
        while search_frontier:
            this = search_frontier.pop()
            for neighbour in self.neighbours(this):
                assert isinstance(neighbour, Byte)
                if neighbour.corrupted:
                    continue
                if neighbour.distance <= this.distance + 1:
                    continue
                neighbour.distance = this.distance + 1
                search_frontier.add(neighbour)

    def calculate_distances(self):
        for byte in self.tiles():
            assert isinstance(byte, Byte)
            byte.distance = 9999
        end = self.end()
        end.distance = 0
        search_frontier = {end}
        while search_frontier:
            this = search_frontier.pop()
            for neighbour in self.neighbours(this):
                assert isinstance(neighbour, Byte)
                if neighbour.corrupted:
                    continue
                if neighbour.distance <= this.distance + 1:
                    continue
                neighbour.distance = this.distance + 1
                search_frontier.add(neighbour)


memory = Memory(71, 71)
for byte in stdin.read().splitlines():
    x, y = map(int, byte.split(","))
    memory.corrupt(y, x)
    memory.calculate_distances()
    if memory.start().distance < 9999:
        continue
    print(x, y)
    break
