from sys import stdin


class Report:

    def __init__(self, levels: list[int]):
        self.levels = levels

    @classmethod
    def from_input(cls, data: str):
        return Report(list(map(int, data.split())))

    def safe(self):
        return self._safe_increasing() or self._safe_decreasing()

    def _safe_increasing(self):
        a = self.levels[0]
        for b in self.levels[1:]:
            if 1 <= (b - a) <= 3:
                a = b
            else:
                return False
        return True

    def _safe_decreasing(self):
        a = self.levels[0]
        for b in self.levels[1:]:
            if 1 <= (a - b) <= 3:
                a = b
            else:
                return False
        return True


levels = list(map(Report.from_input, stdin.readlines()))

n_safe = sum(level.safe() for level in levels)

print(n_safe)
