from enum import Enum
import itertools
from sys import stdin


class Feature(Enum):

    EMPTY = 0
    OBSTACLE = 1
    EXIT = 2


class Position:

    def __init__(self, feature: Feature):
        self.feature = feature
        self.original_feature = feature
        self.collisions = []

    @classmethod
    def from_input(cls, data: str):
        if data == "#":
            return Position(Feature.OBSTACLE)
        return Position(Feature.EMPTY)

    def reset(self):
        self.feature = self.original_feature
        self.collisions.clear()


class Guard:

    def __init__(self, i: int, j: int):
        self.si = i
        self.sj = j
        self.reset()

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

    def reset(self):
        self.i = self.si
        self.j = self.sj
        self.di = -1
        self.dj = 0


class Area:

    def __init__(self, positions: list[list[Position]], guard: Guard):
        self.positions = positions
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

    def reset(self):
        """Reset the area.

        Reset the guard back to its starting position and direction.
        Also, remove any visited markers on positions in the area.
        """
        self.guard.reset()
        for position in itertools.chain(*self.positions):
            position.reset()

    def next_position(self):
        """
        Return the position that the guard will visit next.

        If the guard is about to leave the area, create and return a
        position with an exit feature instead.
        """
        i = self.guard.i + self.guard.di
        j = self.guard.j + self.guard.dj
        if 0 <= i < self.height and 0 <= j < self.width:
            return self.positions[i][j]
        return Position(Feature.EXIT)

    def move_guard(self):
        """
        Move the guard to its next position.

        If the guard faces an obstacle, rotate the guard. Also, mark the
        position the guard moves to as visited.
        """
        while self.next_position().feature == Feature.OBSTACLE:
            next_position = self.next_position()
            if (self.guard.di, self.guard.dj) in next_position.collisions:
                return
            next_position.collisions.append((self.guard.di, self.guard.dj))
            self.guard.rotate()
        self.guard.move()
        while self.next_position().feature == Feature.OBSTACLE:
            next_position = self.next_position()
            if (self.guard.di, self.guard.dj) in next_position.collisions:
                return
            next_position.collisions.append((self.guard.di, self.guard.dj))
            self.guard.rotate()

    def causes_loop(self, i: int, j: int):
        """
        Determine whether blocking (`i`, `j`) would trap the guard.

        The new obstacle cannot be placed at the guard's starting
        position.
        """
        if (i, j) == (self.guard.si, self.guard.sj):
            return False
        self.positions[i][j].feature = Feature.OBSTACLE
        while self.next_position().feature != Feature.EXIT:
            self.move_guard()
            next_position = self.next_position()
            if (self.guard.di, self.guard.dj) in next_position.collisions:
                self.reset()
                return True
        self.reset()
        return False

    def n_loopable_positions(self):
        """Return the number of positions that could cause a loop."""
        return sum(
            int(self.causes_loop(i, j))
            for i in range(self.height)
            for j in range(self.width)
        )


area = Area.from_input(stdin.read())
print(area.n_loopable_positions())
