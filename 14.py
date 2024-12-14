from enum import Enum
import math
from sys import stdin


HEIGHT = 103
WIDTH = 101


class Quadrant(Enum):

    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT = 3


class Robot:

    def __init__(self, i: int, j: int, di: int, dj: int):
        self.i = i
        self.j = j
        self.di = di
        self.dj = dj

    @classmethod
    def from_input(cls, data: str):
        position, velocity = data.split()
        j, i = map(int, position.removeprefix("p=").split(","))
        dj, di = map(int, velocity.removeprefix("v=").split(","))
        return Robot(i, j, di, dj)

    def destination(self, n: int):
        """
        Return this robot's location after moving for `n` seconds.

        Represent this information as a new Robot object with the same
        `di` and `dj`."""
        i = (self.i + (n * self.di)) % HEIGHT
        j = (self.j + (n * self.dj)) % WIDTH
        return Robot(i, j, self.di, self.dj)

    def quadrant(self):
        """
        Return the quadrant that this robot occupies.

        If the robot is not in a quadrant (due to being in the middle),
        return None instead.
        """
        if self.i < HEIGHT // 2 and self.j < WIDTH // 2:
            return Quadrant.TOP_LEFT
        elif self.i < HEIGHT // 2 and self.j > WIDTH // 2:
            return Quadrant.TOP_RIGHT
        elif self.i > HEIGHT // 2 and self.j < WIDTH // 2:
            return Quadrant.BOTTOM_LEFT
        elif self.i > HEIGHT // 2 and self.j > WIDTH // 2:
            return Quadrant.BOTTOM_RIGHT
        else:
            return None


robots = [Robot.from_input(robot) for robot in stdin.read().splitlines()]
quadrants = {quadrant: 0 for quadrant in Quadrant}
for robot in robots:
    quadrant = robot.destination(100).quadrant()
    if quadrant is None:
        continue
    quadrants[quadrant] += 1
print(math.prod(quadrants.values()))
