from enum import Enum
from sys import stdin


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
                self.robot_i = i
                self.robot_j = j
                return
        assert False, "no robot found"

    @classmethod
    def from_input(cls, data: str):
        map_data, movement_data = data.split("\n\n")
        features = [
            [Feature(feature) for feature in row]
            for row in map_data.splitlines()
        ]
        movements = [
            Movement(movement) for movement in movement_data.replace("\n", "")
        ]
        return Warehouse(features, movements)

    def move_robot(self, movement: Movement):

        # Find empty space to move to
        delta_i, delta_j = movement.coordinates()
        initial_i = self.robot_i + delta_i
        initial_j = self.robot_j + delta_j
        target_i = initial_i
        target_j = initial_j
        target_feature = self.features[target_i][target_j]
        while target_feature == Feature.BOX:
            target_i += delta_i
            target_j += delta_j
            target_feature = self.features[target_i][target_j]

        # Don't move if a wall is blocking
        if target_feature == Feature.WALL:
            return

        # Move boxes, if the robot pushed any
        if (target_i, target_j) != (initial_i, initial_j):
            self.features[target_i][target_j] = Feature.BOX

        # Move robot
        self.features[initial_i][initial_j] = Feature.ROBOT
        self.features[self.robot_i][self.robot_j] = Feature.EMPTY
        self.robot_i = initial_i
        self.robot_j = initial_j

    def gps_coordinate_sum(self):
        gps_coordinate_sum = 0
        for i, row in enumerate(self.features):
            for j, feature in enumerate(row):
                if feature != Feature.BOX:
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
