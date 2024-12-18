from typing import Callable


class Tile:
    """
    Represent a tile inside the grid.

    Tiles have at minimum (u, v) coordinates; subclasses may implement
    additional functionality.
    """

    def __init__(self, u: int, v: int):
        self.u = u
        self.v = v

    def __hash__(self):
        return hash((self.u, self.v))

    def display(self):
        """Return a string displaying this tile."""
        return "."


class Grid:
    """
    Represent a grid of tiles.

    The u-axis is vertical, the v-axis is horizontal, and (0, 0) is the
    top-left corner.
    """

    def __init__(self, tiles: list[list[Tile]]):
        """
        Initialise a new grid.

        The list of tiles should be organised by rows, such as:
        ```
        [
            [(0, 0), (0, 1), (0, 2)...]
            [(1, 0), (1, 1), (1, 2)...]
            [(2, 0), (2, 1), (2, 2)...]
            ...
        ]
        ```
        """
        self._tiles = tiles
        self.height = len(tiles)
        self.width = len(tiles[0])

    def tile(self, u: int, v: int):
        """
        Return the tile at (u, v).

        If (u, v) are invalid coordinates, return None instead.
        """
        if not 0 <= u < self.height:
            return None
        if not 0 <= v < self.width:
            return None
        return self._tiles[u][v]

    def tiles(self):
        """Return a list of all tiles."""
        return sum(self._tiles, start=[])

    def neighbours(self, tile: Tile):
        """Return a list of tiles adjacent to `tile`."""
        neighbours = [
            self.tile(tile.u - 1, tile.v),
            self.tile(tile.u + 1, tile.v),
            self.tile(tile.u, tile.v - 1),
            self.tile(tile.u, tile.v + 1),
        ]
        return list(filter(None, neighbours))

    def display(self, function: Callable[[Tile], str] = Tile.display):
        """
        Return a string displaying the grid.

        `function`, if supplied, will be used to decide how to display
        tiles. It should be a callable that returns a string.
        """
        return "\n".join(
            "".join(function(tile) for tile in row) for row in self._tiles
        )
