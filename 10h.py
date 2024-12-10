from sys import stdin


class TopographicMap:

    def __init__(self, positions: list[list[int]]):
        self.positions = positions
        self.height = len(positions)
        self.width = len(positions[0])

    @classmethod
    def from_input(cls, data: str):
        positions = [
            [int(position) for position in row] for row in data.splitlines()
        ]
        return TopographicMap(positions)

    def score(self, i: int, j: int, expected: int = 0) -> int:
        if not 0 <= i < self.height:
            return 0
        if not 0 <= j < self.width:
            return 0
        this = self.positions[i][j]
        if this != expected:
            return 0
        if this == 9:
            return 1
        return (
            self.score(i - 1, j, expected + 1)
            + self.score(i + 1, j, expected + 1)
            + self.score(i, j - 1, expected + 1)
            + self.score(i, j + 1, expected + 1)
        )

    def trailhead_scores(self):
        trailhead_scores = []
        for i, row in enumerate(self.positions):
            for j, position in enumerate(row):
                if position > 0:
                    continue
                trailhead_scores.append(self.score(i, j))
        return trailhead_scores


topographic_map = TopographicMap.from_input(stdin.read())
print(sum(topographic_map.trailhead_scores()))
