from sys import stdin

import grid


class Tile(grid.Tile):
    """
    Represent a tile in the maze.

    Tiles have a score value in each direction, which represents the
    lowest score a reindeer could possibly get reaching this tile and
    facing that direction.
    """

    def __init__(self, u: int, v: int, wall: bool = False):
        super().__init__(u, v)
        if wall:
            self.ns_score = -1
            self.ew_score = -1
        else:
            self.ns_score = 999_999
            self.ew_score = 999_999


class Maze(grid.Grid):

    def __init__(
        self, tiles: list[list[Tile]], su: int, sv: int, eu: int, ev: int
    ):
        super().__init__(tiles)
        self.su = su
        self.sv = sv
        self.eu = eu
        self.ev = ev
        self.search_frontier: set[Tile] = set()

    @classmethod
    def from_input(cls, data: str):
        tiles: list[list[Tile]] = []
        for u, data_row in enumerate(data.splitlines()):
            tile_row: list[Tile] = []
            for v, tile in enumerate(data_row):
                if tile == "S":
                    su = u
                    sv = v
                    tile_row.append(Tile(u, v))
                elif tile == "E":
                    eu = u
                    ev = v
                    tile_row.append(Tile(u, v))
                elif tile == ".":
                    tile_row.append(Tile(u, v))
                elif tile == "#":
                    tile_row.append(Tile(u, v, wall=True))
                else:
                    assert False
            tiles.append(tile_row)
        return Maze(tiles, su, sv, eu, ev)

    def start(self) -> Tile:
        return self.tile(self.su, self.sv)

    def end(self) -> Tile:
        return self.tile(self.eu, self.ev)

    def calculate_scores(self):
        start = self.start()
        start.ns_score = 1000
        start.ew_score = 0
        self.search_frontier = {start}
        while self.search_frontier:
            this = self.search_frontier.pop()
            self._update_ns_neighbour(this, self.tile(this.u - 1, this.v))
            self._update_ns_neighbour(this, self.tile(this.u + 1, this.v))
            self._update_ew_neighbour(this, self.tile(this.u, this.v - 1))
            self._update_ew_neighbour(this, self.tile(this.u, this.v + 1))

    def _update_ns_neighbour(self, tile: Tile, neighbour: Tile | None):
        if neighbour is None:
            return
        if neighbour.ns_score > tile.ns_score + 1:
            neighbour.ns_score = tile.ns_score + 1
            self.search_frontier.add(neighbour)
        if neighbour.ns_score > tile.ew_score + 1001:
            neighbour.ns_score = tile.ew_score + 1001
            self.search_frontier.add(neighbour)

    def _update_ew_neighbour(self, tile: Tile, neighbour: Tile | None):
        if neighbour is None:
            return
        if neighbour.ew_score > tile.ew_score + 1:
            neighbour.ew_score = tile.ew_score + 1
            self.search_frontier.add(neighbour)
        if neighbour.ew_score > tile.ns_score + 1001:
            neighbour.ew_score = tile.ns_score + 1001
            self.search_frontier.add(neighbour)

    def end_score(self):
        end = self.end()
        return min(end.ns_score, end.ew_score)


maze = Maze.from_input(stdin.read())
maze.calculate_scores()
print(maze.end_score())
