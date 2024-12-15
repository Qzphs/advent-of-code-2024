from enum import Enum
from sys import stdin


class Feature(Enum):

    EMPTY = "."
    WALL = "#"
    BOX_LEFT = "["
    BOX_RIGHT = "]"
    ROBOT = "@"


class Movement(Enum):

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def coordinates(self) -> tuple[int, int]:
        if self == Movement.UP:
            return (-1, 0)
        elif self == Movement.DOWN:
            return (1, 0)
        elif self == Movement.LEFT:
            return (0, -1)
        elif self == Movement.RIGHT:
            return (0, 1)


class Warehouse:

    def __init__(
        self, features: list[list[Feature]], movements: list[Movement]
    ):
        self.features = features
        self.movements = movements
        self._init_robot()
        self.height = len(self.features)
        self.width = len(self.features[0])

    def _init_robot(self):
        for i, row in enumerate(self.features):
            for j, feature in enumerate(row):
                if feature != Feature.ROBOT:
                    continue
                self.ri = i
                self.rj = j
                return
        assert False, "no robot found"

    @classmethod
    def from_input(cls, data: str):
        map_data, movement_data = data.split("\n\n")
        features: list[list[Feature]] = []
        for data_row in map_data.splitlines():
            feature_row: list[Feature] = []
            for feature in data_row:
                if feature == ".":
                    feature_row.append(Feature.EMPTY)
                    feature_row.append(Feature.EMPTY)
                elif feature == "#":
                    feature_row.append(Feature.WALL)
                    feature_row.append(Feature.WALL)
                elif feature == "O":
                    feature_row.append(Feature.BOX_LEFT)
                    feature_row.append(Feature.BOX_RIGHT)
                elif feature == "@":
                    feature_row.append(Feature.ROBOT)
                    feature_row.append(Feature.EMPTY)
                else:
                    assert False
            features.append(feature_row)
        movements = [
            Movement(movement) for movement in movement_data.replace("\n", "")
        ]
        return Warehouse(features, movements)

    def move_robot(self, movement: Movement):
        di, dj = movement.coordinates()
        if not self.pushable(self.ri, self.rj, di, dj):
            return
        self.push(self.ri, self.rj, di, dj)
        self.ri += di
        self.rj += dj

    def pushable(self, oi: int, oj: int, di: int, dj: int) -> bool:
        """
        Return True if (oi, oj) can be pushed in direction (di, dj).

        The pusher is located at (oi - di, oj - dj), and wants to
        occupy (oi, oj), pushing the feature here to (oi + di, oj + dj).

        Empty spaces don't need to occupy anything and are considered
        always pushable by default.
        """
        feature = self.features[oi][oj]
        if feature == Feature.EMPTY:
            return True
        elif feature == Feature.WALL:
            return False
        elif feature == Feature.BOX_LEFT and di == 0:
            return self.pushable(oi + di, oj + dj + 1, di, dj)
        elif feature == Feature.BOX_RIGHT and di == 0:
            return self.pushable(oi + di, oj + dj - 1, di, dj)
        elif feature == Feature.BOX_LEFT and dj == 0:
            return self.pushable(oi + di, oj + dj, di, dj) and self.pushable(
                oi + di, oj + dj + 1, di, dj
            )
        elif feature == Feature.BOX_RIGHT and dj == 0:
            return self.pushable(oi + di, oj + dj, di, dj) and self.pushable(
                oi + di, oj + dj - 1, di, dj
            )
        elif feature == Feature.ROBOT:
            return self.pushable(oi + di, oj + dj, di, dj)
        else:
            assert False

    def push(self, oi: int, oj: int, di: int, dj: int):
        feature = self.features[oi][oj]
        if feature == Feature.EMPTY:
            return
        elif feature == Feature.BOX_LEFT and di == 0:
            self.push(oi + di, oj + dj + 1, di, dj)
            self.features[oi + di][oj + dj] = Feature.BOX_LEFT
            self.features[oi + di][oj + dj + 1] = Feature.BOX_RIGHT
            self.features[oi][oj] = Feature.EMPTY
        elif feature == Feature.BOX_RIGHT and di == 0:
            self.push(oi + di, oj + dj - 1, di, dj)
            self.features[oi + di][oj + dj] = Feature.BOX_RIGHT
            self.features[oi + di][oj + dj - 1] = Feature.BOX_LEFT
            self.features[oi][oj] = Feature.EMPTY
        elif feature == Feature.BOX_LEFT and dj == 0:
            self.push(oi + di, oj + dj, di, dj)
            self.push(oi + di, oj + dj + 1, di, dj)
            self.features[oi + di][oj + dj] = Feature.BOX_LEFT
            self.features[oi + di][oj + dj + 1] = Feature.BOX_RIGHT
            self.features[oi][oj] = Feature.EMPTY
            self.features[oi][oj + 1] = Feature.EMPTY
        elif feature == Feature.BOX_RIGHT and dj == 0:
            self.push(oi + di, oj + dj, di, dj)
            self.push(oi + di, oj + dj - 1, di, dj)
            self.features[oi + di][oj + dj] = Feature.BOX_RIGHT
            self.features[oi + di][oj + dj - 1] = Feature.BOX_LEFT
            self.features[oi][oj] = Feature.EMPTY
            self.features[oi][oj - 1] = Feature.EMPTY
        elif feature == Feature.ROBOT:
            self.push(oi + di, oj + dj, di, dj)
            self.features[oi + di][oj + dj] = Feature.ROBOT
            self.features[oi][oj] = Feature.EMPTY
        else:
            assert False

    def gps_coordinate_sum(self):
        gps_coordinate_sum = 0
        for i, row in enumerate(self.features):
            for j, feature in enumerate(row):
                if feature != Feature.BOX_LEFT:
                    continue
                gps_coordinate_sum += (100 * i) + j
        return gps_coordinate_sum

    def box_locations(self):
        return "\n".join(
            "".join(feature.value for feature in row) for row in self.features
        )


warehouse = Warehouse.from_input(stdin.read())
for movement in warehouse.movements:
    warehouse.move_robot(movement)
print(warehouse.gps_coordinate_sum())
