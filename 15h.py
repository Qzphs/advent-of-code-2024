from enum import Enum
from sys import stdin

from grid import Grid, GridTile


class Feature(Enum):

    EMPTY = "."
    WALL = "#"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    ROBOT = "@"

    @classmethod
    def pair_from_input(cls, data: str):
        if data == ".":
            return [Feature.EMPTY, Feature.EMPTY]
        elif data == "#":
            return [Feature.WALL, Feature.WALL]
        elif data == "O":
            return [Feature.BOX_LEFT, Feature.BOX_RIGHT]
        elif data == "@":
            return [Feature.ROBOT, Feature.EMPTY]
        else:
            assert False, f"unrecognised feature {data}"


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

    @classmethod
    def pair(cls, u: int, v: int, features: list[Feature]):
        left, right = features
        return [
            WarehouseTile(u, v * 2, left),
            WarehouseTile(u, v * 2 + 1, right),
        ]

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
            sum(
                (
                    WarehouseTile.pair(u, v, Feature.pair_from_input(feature))
                    for v, feature in enumerate(row)
                ),
                start=[],
            )
            for u, row in enumerate(map_part.splitlines())
        ]
        movements = [
            Movement(movement) for movement in movement_part.replace("\n", "")
        ]
        return Warehouse(tiles, movements)

    def move_robot(self, movement: Movement):
        if not self.pushable(self.ru, self.rv, movement):
            return
        self.push(self.ru, self.rv, movement)
        self.ru += movement.u
        self.rv += movement.v

    def pushable(self, ou: int, ov: int, movement: Movement) -> bool:
        """
        Return True if (ou, ov) can be pushed in (du, dv).

        (du, dv) is the direction of movement.

        The pusher is located at (ou - du, ov - dv) and wants to occupy
        (ou, ov), pushing the feature here to (ou + du, ov + dv).

        Empty spaces don't need to occupy anything and are considered
        always pushable by default.
        """
        du = movement.u
        dv = movement.v
        origin = self.tile(ou, ov)
        if origin.feature == Feature.EMPTY:
            return True
        elif origin.feature == Feature.WALL:
            return False
        elif origin.feature == Feature.BOX_LEFT and du == 0:
            return self.pushable(ou + du, ov + dv + 1, movement)
        elif origin.feature == Feature.BOX_RIGHT and du == 0:
            return self.pushable(ou + du, ov + dv - 1, movement)
        elif origin.feature == Feature.BOX_LEFT and dv == 0:
            return self.pushable(ou + du, ov + dv, movement) and self.pushable(
                ou + du, ov + dv + 1, movement
            )
        elif origin.feature == Feature.BOX_RIGHT and dv == 0:
            return self.pushable(ou + du, ov + dv, movement) and self.pushable(
                ou + du, ov + dv - 1, movement
            )
        elif origin.feature == Feature.ROBOT:
            return self.pushable(ou + du, ov + dv, movement)
        else:
            assert False

    def push(self, ou: int, ov: int, movement: Movement):
        du = movement.u
        dv = movement.v
        origin = self.tile(ou, ov)
        if origin.feature == Feature.EMPTY:
            return
        elif origin.feature == Feature.BOX_LEFT and du == 0:
            self.push(ou + du, ov + dv + 1, movement)
            self.tile(ou + du, ov + dv).feature = Feature.BOX_LEFT
            self.tile(ou + du, ov + dv + 1).feature = Feature.BOX_RIGHT
            self.tile(ou, ov).feature = Feature.EMPTY
        elif origin.feature == Feature.BOX_RIGHT and du == 0:
            self.push(ou + du, ov + dv - 1, movement)
            self.tile(ou + du, ov + dv).feature = Feature.BOX_RIGHT
            self.tile(ou + du, ov + dv - 1).feature = Feature.BOX_LEFT
            self.tile(ou, ov).feature = Feature.EMPTY
        elif origin.feature == Feature.BOX_LEFT and dv == 0:
            self.push(ou + du, ov + dv, movement)
            self.push(ou + du, ov + dv + 1, movement)
            self.tile(ou + du, ov + dv).feature = Feature.BOX_LEFT
            self.tile(ou + du, ov + dv + 1).feature = Feature.BOX_RIGHT
            self.tile(ou, ov).feature = Feature.EMPTY
            self.tile(ou, ov + 1).feature = Feature.EMPTY
        elif origin.feature == Feature.BOX_RIGHT and dv == 0:
            self.push(ou + du, ov + dv, movement)
            self.push(ou + du, ov + dv - 1, movement)
            self.tile(ou + du, ov + dv).feature = Feature.BOX_RIGHT
            self.tile(ou + du, ov + dv - 1).feature = Feature.BOX_LEFT
            self.tile(ou, ov).feature = Feature.EMPTY
            self.tile(ou, ov - 1).feature = Feature.EMPTY
        elif origin.feature == Feature.ROBOT:
            self.push(ou + du, ov + dv, movement)
            self.tile(ou + du, ov + dv).feature = Feature.ROBOT
            self.tile(ou, ov).feature = Feature.EMPTY
        else:
            assert False

    def gps_coordinate_sum(self):
        return sum(
            (100 * tile.u) + tile.v
            for tile in self.tiles()
            if tile.feature == Feature.BOX_LEFT
        )


warehouse = Warehouse.from_input(stdin.read())
for movement in warehouse.movements:
    warehouse.move_robot(movement)
print(warehouse.gps_coordinate_sum())
