import itertools
from sys import stdin


class Antenna:

    def __init__(self, frequency: str, i: int, j: int):
        self.frequency = frequency
        self.i = i
        self.j = j


class City:

    def __init__(self, height: int, width: int):
        self.antennae: dict[str, list[Antenna]] = {}
        self.antinodes = [[False] * width for _ in range(height)]
        self.height = height
        self.width = width

    def add_antenna(self, antenna: Antenna):
        if antenna.frequency not in self.antennae.keys():
            self.antennae[antenna.frequency] = []
        self.antennae[antenna.frequency].append(antenna)

    def add_antinode(self, i: int, j: int):
        if not 0 <= i < self.height:
            return
        if not 0 <= j < self.width:
            return
        self.antinodes[i][j] = True

    @classmethod
    def from_input(cls, data: str):
        rows = data.splitlines()
        city = City(len(rows), len(rows[0]))
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if cell == ".":
                    continue
                city.add_antenna(Antenna(cell, i, j))
        return city

    def create_antinodes(self):
        for antennae in self.antennae.values():
            for a1, a2 in itertools.combinations(antennae, 2):
                di = a1.i - a2.i
                dj = a1.j - a2.j
                self.add_antinode(a1.i + di, a1.j + dj)
                self.add_antinode(a2.i - di, a2.j - dj)

    def n_antinodes(self):
        return sum(itertools.chain(*self.antinodes))


city = City.from_input(stdin.read())
city.create_antinodes()
print(city.n_antinodes())
