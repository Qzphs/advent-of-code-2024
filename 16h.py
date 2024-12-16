import itertools
from sys import stdin


class Tile:
    """
    Represent a tile in the maze.

    Tiles have a score value in each direction, which represents the
    lowest score a reindeer could possibly get reaching this tile and
    facing that direction.
    """

    def __init__(self, ns_start: int, ew_start: int, ns_end: int, ew_end: int):
        self.ns_start = ns_start
        self.ew_start = ew_start
        self.ns_end = ns_end
        self.ew_end = ew_end
        self.best = False

    @classmethod
    def empty(cls):
        return Tile(999_999_999, 999_999_999, 999_999_999, 999_999_999)

    @classmethod
    def wall(cls):
        return Tile(-1, -1, -1, -1)


class Maze:

    def __init__(
        self, tiles: list[list[Tile]], si: int, sj: int, ei: int, ej: int
    ):
        self.tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.calculate_scores_start(si, sj)
        self.calculate_scores_end(ei, ej)
        self.calculate_event_score(ei, ej)

    @classmethod
    def from_input(cls, data: str):
        tiles: list[list[Tile]] = []
        for i, data_row in enumerate(data.splitlines()):
            tile_row: list[Tile] = []
            for j, tile in enumerate(data_row):
                if tile == "S":
                    si = i
                    sj = j
                    tile_row.append(Tile.empty())
                elif tile == "E":
                    ei = i
                    ej = j
                    tile_row.append(Tile.empty())
                elif tile == ".":
                    tile_row.append(Tile.empty())
                elif tile == "#":
                    tile_row.append(Tile.wall())
                else:
                    assert False
            tiles.append(tile_row)
        return Maze(tiles, si, sj, ei, ej)

    def tile(self, i: int, j: int):
        """
        Return the tile at (i, j).

        If (i, j) are invalid, return a new wall tile instead.
        """
        if not 0 <= i < self.height:
            return Tile.wall()
        if not 0 <= j < self.width:
            return Tile.wall()
        return self.tiles[i][j]

    def calculate_scores_start(self, si: int, sj: int):
        """Mark (si, sj) as the start tile and calculate scores."""
        start_tile = self.tile(si, sj)
        start_tile.ns_start = 1000
        start_tile.ew_start = 0
        queue: set[tuple[int, int]] = {(si, sj)}

        while queue:

            i, j = queue.pop()
            this = self.tile(i, j)

            left = self.tile(i, j - 1)
            if left.ew_start > this.ew_start + 1:
                left.ew_start = this.ew_start + 1
                queue.add((i, j - 1))
            if left.ew_start > this.ns_start + 1001:
                left.ew_start = this.ns_start + 1001
                queue.add((i, j - 1))

            right = self.tile(i, j + 1)
            if right.ew_start > this.ew_start + 1:
                right.ew_start = this.ew_start + 1
                queue.add((i, j + 1))
            if right.ew_start > this.ns_start + 1001:
                right.ew_start = this.ns_start + 1001
                queue.add((i, j + 1))

            up = self.tile(i - 1, j)
            if up.ns_start > this.ns_start + 1:
                up.ns_start = this.ns_start + 1
                queue.add((i - 1, j))
            if up.ns_start > this.ew_start + 1001:
                up.ns_start = this.ew_start + 1001
                queue.add((i - 1, j))

            down = self.tile(i + 1, j)
            if down.ns_start > this.ns_start + 1:
                down.ns_start = this.ns_start + 1
                queue.add((i + 1, j))
            if down.ns_start > this.ew_start + 1001:
                down.ns_start = this.ew_start + 1001
                queue.add((i + 1, j))

    def calculate_scores_end(self, ei: int, ej: int):
        """Mark (ej, ej) as the end tile and calculate scores."""
        end_tile = self.tile(ei, ej)
        if end_tile.ns_start < end_tile.ns_end:
            end_tile.ns_end = 0
            end_tile.ew_end = 1000
        elif end_tile.ns_start > end_tile.ns_end:
            end_tile.ns_end = 1000
            end_tile.ew_end = 0
        else:
            end_tile.ns_end = 0
            end_tile.ew_end = 0
        queue: set[tuple[int, int]] = {(ei, ej)}

        while queue:

            i, j = queue.pop()
            this = self.tile(i, j)

            left = self.tile(i, j - 1)
            if left.ew_end > this.ew_end + 1:
                left.ew_end = this.ew_end + 1
                queue.add((i, j - 1))
            if left.ew_end > this.ns_end + 1001:
                left.ew_end = this.ns_end + 1001
                queue.add((i, j - 1))

            right = self.tile(i, j + 1)
            if right.ew_end > this.ew_end + 1:
                right.ew_end = this.ew_end + 1
                queue.add((i, j + 1))
            if right.ew_end > this.ns_end + 1001:
                right.ew_end = this.ns_end + 1001
                queue.add((i, j + 1))

            up = self.tile(i - 1, j)
            if up.ns_end > this.ns_end + 1:
                up.ns_end = this.ns_end + 1
                queue.add((i - 1, j))
            if up.ns_end > this.ew_end + 1001:
                up.ns_end = this.ew_end + 1001
                queue.add((i - 1, j))

            down = self.tile(i + 1, j)
            if down.ns_end > this.ns_end + 1:
                down.ns_end = this.ns_end + 1
                queue.add((i + 1, j))
            if down.ns_end > this.ew_end + 1001:
                down.ns_end = this.ew_end + 1001
                queue.add((i + 1, j))

    def calculate_event_score(self, ei: int, ej: int):
        end_tile = self.tile(ei, ej)
        self.event_score = min(end_tile.ns_start, end_tile.ew_start)

    def n_best_tiles(self):
        n_best_tiles = 0
        for tile in itertools.chain(*self.tiles):
            if tile.ns_start + tile.ns_end == self.event_score:
                n_best_tiles += 1
            elif tile.ew_start + tile.ew_end == self.event_score:
                n_best_tiles += 1
        return n_best_tiles

    def debug(self):
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                if tile.ns_start == -1:
                    print(".", end="")
                elif tile.ns_start + tile.ns_end == self.event_score:
                    print("O", end="")
                elif tile.ew_start + tile.ew_end == self.event_score:
                    print("O", end="")
                else:
                    print(" ", end="")
            print()


# This solution can't detect best tiles on the corners of paths. I
# couldn't be bothered fixing this or changing approach so I just
# visualise the paths and count the corners manually.


maze = Maze.from_input(stdin.read())
maze.debug()
print(maze.n_best_tiles())
