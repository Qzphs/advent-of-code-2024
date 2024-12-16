from sys import stdin


class Tile:
    """
    Represent a tile in the maze.

    Tiles have a score value in each direction, which represents the
    lowest score a reindeer could possibly get reaching this tile and
    facing that direction.
    """

    def __init__(self, ns_score: int, ew_score: int):
        self.ns_score = ns_score
        self.ew_score = ew_score

    @classmethod
    def empty(cls):
        return Tile(999_999_999, 999_999_999)

    @classmethod
    def wall(cls):
        return Tile(-1, -1)


class Maze:

    def __init__(
        self, tiles: list[list[Tile]], si: int, sj: int, ei: int, ej: int
    ):
        self.tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.calculate_scores(si, sj)
        end_tile = self.tile(ei, ej)
        self.end_score = min(end_tile.ns_score, end_tile.ew_score)

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

    def calculate_scores(self, si: int, sj: int):
        """Mark (si, sj) as the start tile and calculate scores."""
        self.tile(si, sj).ns_score = 1000
        self.tile(si, sj).ew_score = 0
        queue: set[tuple[int, int]] = {(si, sj)}

        while queue:

            i, j = queue.pop()
            this = self.tile(i, j)

            left = self.tile(i, j - 1)
            if left.ew_score > this.ew_score + 1:
                left.ew_score = this.ew_score + 1
                queue.add((i, j - 1))
            if left.ew_score > this.ns_score + 1001:
                left.ew_score = this.ns_score + 1001
                queue.add((i, j - 1))

            right = self.tile(i, j + 1)
            if right.ew_score > this.ew_score + 1:
                right.ew_score = this.ew_score + 1
                queue.add((i, j + 1))
            if right.ew_score > this.ns_score + 1001:
                right.ew_score = this.ns_score + 1001
                queue.add((i, j + 1))

            up = self.tile(i - 1, j)
            if up.ns_score > this.ns_score + 1:
                up.ns_score = this.ns_score + 1
                queue.add((i - 1, j))
            if up.ns_score > this.ew_score + 1001:
                up.ns_score = this.ew_score + 1001
                queue.add((i - 1, j))

            down = self.tile(i + 1, j)
            if down.ns_score > this.ns_score + 1:
                down.ns_score = this.ns_score + 1
                queue.add((i + 1, j))
            if down.ns_score > this.ew_score + 1001:
                down.ns_score = this.ew_score + 1001
                queue.add((i + 1, j))


maze = Maze.from_input(stdin.read())
print(maze.end_score)
