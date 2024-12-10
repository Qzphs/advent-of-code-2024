from enum import Enum
import itertools
from sys import stdin


class Feature(Enum):

    EMPTY = 0
    OBSTACLE = 1


class Position:

    def __init__(self, feature: Feature):
        self.feature = feature
        self.visited = False

    @classmethod
    def from_input(cls, data: str):
        if data == "#":
            return Position(Feature.OBSTACLE)
        return Position(Feature.EMPTY)

    def visit(self):
        self.visited = True


class Guard:

    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        self.di = -1
        self.dj = 0

    @classmethod
    def from_input(cls, data: str):
        for i, row in enumerate(data.splitlines()):
            for j, position in enumerate(row):
                if position == "^":
                    return Guard(i, j)
        assert False, "no guard in input data"

    def move(self):
        self.i += self.di
        self.j += self.dj

    def rotate(self):
        self.di, self.dj = (self.dj, -self.di)


class Area:

    def __init__(self, positions: list[list[Position]], guard: Guard):
        self.positions = positions
        self.positions[guard.i][guard.j].visit()
        self.guard = guard

    @classmethod
    def from_input(cls, data: str):
        return Area(
            [
                [Position.from_input(position) for position in row]
                for row in data.splitlines()
            ],
            Guard.from_input(data),
        )

    @property
    def height(self):
        return len(self.positions)

    @property
    def width(self):
        return len(self.positions[0])

    def next_position(self):
        """
        Return the position that the guard will visit next.

        If the guard is about to leave the area, return None instead.
        """
        i = self.guard.i + self.guard.di
        j = self.guard.j + self.guard.dj
        if 0 <= i < self.height and 0 <= j < self.width:
            return self.positions[i][j]
        return None

    def move_guard(self):
        """
        Move the guard to its next position.

        Mark the position the guard moves to as visited.

        After moving, if the guard faces an obstacle, rotate the guard.
        """
        self.next_position().visit()
        self.guard.move()
        if self.next_position() is None:
            return
        if self.next_position().feature == Feature.OBSTACLE:
            self.guard.rotate()

    def n_visited(self):
        """Return the number of positions the guard has visited."""
        return sum(
            int(position.visited)
            for position in itertools.chain(*self.positions)
        )


area = Area.from_input(stdin.read())
while area.next_position() is not None:
    area.move_guard()
print(area.n_visited())
