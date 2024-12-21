from enum import Enum
from sys import stdin
from grid import Grid, GridTile


class Feature(Enum):

    TRACK = "."
    WALL = "#"


class Position(GridTile):

    def __init__(self, u: int, v: int, feature: Feature):
        super().__init__(u, v)
        self.feature = feature
        self.racetrack_start = False
        self.racetrack_end = False
        self.distance = 99999

    @classmethod
    def from_input(cls, u: int, v: int, data: str):
        position = Position(u, v, Feature.TRACK)
        if data == "#":
            position.feature = Feature.WALL
        elif data == "S":
            position.racetrack_start = True
        elif data == "E":
            position.racetrack_end = True
        return position


class Racetrack(Grid[Position]):

    def __init__(self, positions: list[list[Position]]):
        super().__init__(positions)
        self.start = self._find_race_start()
        self.end = self._find_race_end()
        self._run_race_legitimately()

    @classmethod
    def from_input(cls, data: str):
        positions = [
            [
                Position.from_input(u, v, feature)
                for v, feature in enumerate(row)
            ]
            for u, row in enumerate(data.splitlines())
        ]
        return Racetrack(positions)

    def _find_race_start(self):
        for tile in self.tiles():
            if not tile.racetrack_start:
                continue
            return tile
        assert False, "no start position"

    def _find_race_end(self):
        for tile in self.tiles():
            if not tile.racetrack_end:
                continue
            return tile
        assert False, "no end position"

    def _run_race_legitimately(self):
        for tile in self.tiles():
            tile.distance = 99999
        self.start.distance = 0
        search_frontier = {self.start}
        while search_frontier:
            this = search_frontier.pop()
            for neighbour in self.neighbours(this):
                if neighbour.feature == Feature.WALL:
                    continue
                if neighbour.distance <= this.distance + 1:
                    continue
                neighbour.distance = this.distance + 1
                search_frontier.add(neighbour)

    def cheats(self):
        for start in self.tiles():
            for end in self._cheat_ends(start):
                if start.feature == Feature.WALL:
                    continue
                if end.feature == Feature.WALL:
                    continue
                yield (start, end)

    def _cheat_ends(self, start: Position):
        positions = [
            self.tile(start.u - 2, start.v),
            self.tile(start.u + 2, start.v),
            self.tile(start.u, start.v - 2),
            self.tile(start.u, start.v + 2),
        ]
        return list(filter(None, positions))

    def cheat_length(self, cheat: tuple[Position, Position]):
        start, end = cheat
        return end.distance - start.distance - 2

    def fast_cheats(self):
        result = []
        for cheat in self.cheats():
            cheat_length = self.cheat_length(cheat)
            if cheat_length < 100:
                continue
            result.append(cheat)
        return result


racetrack = Racetrack.from_input(stdin.read())
print(len(racetrack.fast_cheats()))
