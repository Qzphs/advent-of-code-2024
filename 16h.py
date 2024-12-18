from sys import stdin

from grid import Grid, GridTile


class MazeTile(GridTile):
    """
    Represent a tile in the maze.

    Tiles have a score value in each direction, which represents the
    lowest score a reindeer could possibly get reaching this tile and
    facing that direction.
    """

    def __init__(self, u: int, v: int, wall: bool = False):
        super().__init__(u, v)
        if wall:
            self.ns_start = -1
            self.ew_start = -1
            self.ns_end = -1
            self.ew_end = -1
        else:
            self.ns_start = 999_999
            self.ew_start = 999_999
            self.ns_end = 999_999
            self.ew_end = 999_999

    def display(self):
        if self.ns_start == -1:
            return "."
        else:
            return " "


class Maze(Grid[MazeTile]):

    def __init__(
        self, tiles: list[list[MazeTile]], su: int, sv: int, eu: int, ev: int
    ):
        super().__init__(tiles)
        self.su = su
        self.sv = sv
        self.eu = eu
        self.ev = ev
        self.search_frontier: set[MazeTile] = set()

    @classmethod
    def from_input(cls, data: str):
        tiles: list[list[MazeTile]] = []
        for u, data_row in enumerate(data.splitlines()):
            tile_row: list[MazeTile] = []
            for v, tile in enumerate(data_row):
                if tile == "S":
                    su = u
                    sv = v
                    tile_row.append(MazeTile(u, v))
                elif tile == "E":
                    eu = u
                    ev = v
                    tile_row.append(MazeTile(u, v))
                elif tile == ".":
                    tile_row.append(MazeTile(u, v))
                elif tile == "#":
                    tile_row.append(MazeTile(u, v, wall=True))
                else:
                    assert False
            tiles.append(tile_row)
        return Maze(tiles, su, sv, eu, ev)

    def start(self):
        return self.tile(self.su, self.sv)

    def end(self):
        return self.tile(self.eu, self.ev)

    def calculate_scores_from_start(self):
        start = self.start()
        start.ns_start = 1000
        start.ew_start = 0
        self.search_frontier = {start}
        while self.search_frontier:
            this = self.search_frontier.pop()
            self._update_ns_start(this, self.tile(this.u - 1, this.v))
            self._update_ns_start(this, self.tile(this.u + 1, this.v))
            self._update_ew_start(this, self.tile(this.u, this.v - 1))
            self._update_ew_start(this, self.tile(this.u, this.v + 1))

    def _update_ns_start(self, tile: MazeTile, neighbour: MazeTile | None):
        if neighbour is None:
            return
        if neighbour.ns_start > tile.ns_start + 1:
            neighbour.ns_start = tile.ns_start + 1
            self.search_frontier.add(neighbour)
        if neighbour.ns_start > tile.ew_start + 1001:
            neighbour.ns_start = tile.ew_start + 1001
            self.search_frontier.add(neighbour)

    def _update_ew_start(self, tile: MazeTile, neighbour: MazeTile | None):
        if neighbour is None:
            return
        if neighbour.ew_start > tile.ew_start + 1:
            neighbour.ew_start = tile.ew_start + 1
            self.search_frontier.add(neighbour)
        if neighbour.ew_start > tile.ns_start + 1001:
            neighbour.ew_start = tile.ns_start + 1001
            self.search_frontier.add(neighbour)

    def calculate_scores_from_end(self):
        end = self.end()
        if end.ns_start < end.ns_end:
            end.ns_end = 0
            end.ew_end = 1000
        elif end.ns_start > end.ns_end:
            end.ns_end = 1000
            end.ew_end = 0
        else:
            end.ns_end = 0
            end.ew_end = 0
        self.search_frontier = {end}
        while self.search_frontier:
            this = self.search_frontier.pop()
            self._update_ns_end(this, self.tile(this.u - 1, this.v))
            self._update_ns_end(this, self.tile(this.u + 1, this.v))
            self._update_ew_end(this, self.tile(this.u, this.v - 1))
            self._update_ew_end(this, self.tile(this.u, this.v + 1))

    def _update_ns_end(self, tile: MazeTile, neighbour: MazeTile | None):
        if neighbour is None:
            return
        if neighbour.ns_end > tile.ns_end + 1:
            neighbour.ns_end = tile.ns_end + 1
            self.search_frontier.add(neighbour)
        if neighbour.ns_end > tile.ew_end + 1001:
            neighbour.ns_end = tile.ew_end + 1001
            self.search_frontier.add(neighbour)

    def _update_ew_end(self, tile: MazeTile, neighbour: MazeTile | None):
        if neighbour is None:
            return
        if neighbour.ew_end > tile.ew_end + 1:
            neighbour.ew_end = tile.ew_end + 1
            self.search_frontier.add(neighbour)
        if neighbour.ew_end > tile.ns_end + 1001:
            neighbour.ew_end = tile.ns_end + 1001
            self.search_frontier.add(neighbour)

    def event_score(self):
        end = self.end()
        return min(end.ns_start, end.ew_start)

    def on_path(self, tile: MazeTile):
        end = self.end()
        event_score = min(end.ns_start, end.ew_start)
        return (
            tile.ns_start + tile.ns_end == event_score
            or tile.ew_start + tile.ew_end == event_score
            or tile.ns_start + tile.ew_end + 1000 == event_score
            or tile.ew_start + tile.ns_end + 1000 == event_score
        )

    def n_best_tiles(self):
        return sum(1 for tile in self.tiles() if self.on_path(tile))


maze = Maze.from_input(stdin.read())
maze.calculate_scores_from_start()
maze.calculate_scores_from_end()
print(maze.n_best_tiles())
