from enum import Enum
from sys import stdin

from grid import Grid, GridTile


class Feature(Enum):

    EMPTY = "."
    WALL = "#"
    BOX = "O"
    ROBOT = "@"


class Movement(Enum):

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    @property
    def u(self):
        if self == Movement.UP:
            return -1
        if self == Movement.DOWN:
            return 1
        return 0

    @property
    def v(self):
        if self == Movement.LEFT:
            return -1
        if self == Movement.RIGHT:
            return 1
        return 0


class WarehouseTile(GridTile):

    def __init__(self, u: int, v: int, feature: Feature):
        super().__init__(u, v)
        self.feature = feature

    def display(self):
        return self.feature.value


class Warehouse(Grid[WarehouseTile]):

    def __init__(
        self, tiles: list[list[WarehouseTile]], movements: list[Movement]
    ):
        super().__init__(tiles)
        self._init_robot()
        self.movements = movements

    def _init_robot(self):
        for tile in self.tiles():
            if tile.feature != Feature.ROBOT:
                continue
            self.ru = tile.u
            self.rv = tile.v
            return
        assert False, "no robot in warehouse"

    @classmethod
    def from_input(cls, data: str):
        map_part, movement_part = data.split("\n\n")
        tiles = [
            [
                WarehouseTile(u, v, Feature(feature))
                for v, feature in enumerate(row)
            ]
            for u, row in enumerate(map_part.splitlines())
        ]
        movements = [
            Movement(movement) for movement in movement_part.replace("\n", "")
        ]
        return Warehouse(tiles, movements)

    def move_robot(self, movement: Movement):

        # Find empty space to move to
        iu = self.ru + movement.u
        iv = self.rv + movement.v
        tu = iu
        tv = iv
        target = self.tile(tu, tv)
        while target.feature == Feature.BOX:
            tu += movement.u
            tv += movement.v
            target = self.tile(tu, tv)

        # Don't move if a wall is blocking
        if target.feature == Feature.WALL:
            return

        # Move boxes, if the robot pushed any
        if (tu, tv) != (iu, iv):
            self.tile(tu, tv).feature = Feature.BOX

        # Move robot
        self.tile(iu, iv).feature = Feature.ROBOT
        self.tile(self.ru, self.rv).feature = Feature.EMPTY
        self.ru = iu
        self.rv = iv

    def gps_coordinate_sum(self):
        return sum(
            (100 * tile.u) + tile.v
            for tile in self.tiles()
            if tile.feature == Feature.BOX
        )


warehouse = Warehouse.from_input(stdin.read())
for movement in warehouse.movements:
    warehouse.move_robot(movement)
print(warehouse.gps_coordinate_sum())
