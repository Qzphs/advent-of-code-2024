import itertools
from sys import stdin


class Report:

    def __init__(self, levels: list[int]):
        self.levels = levels

    @classmethod
    def from_input(cls, data: str):
        return Report(list(map(int, data.split())))

    def excluding(self, index: int):
        """Return a copy without the level at `index`."""
        return Report(self.levels[:index] + self.levels[index + 1 :])

    def inverted(self):
        """Return a copy with all levels inverted."""
        return Report([-level for level in self.levels])

    def safe(self):
        """
        Determine whether this report is safe.

        A report is strictly safe if all levels are strictly increasing
        or decreasing, and consecutive levels are 1-3 apart, possibly
        with one level removed.
        """
        conflict = self.conflict()
        if conflict is None:
            return True
        if self.excluding(conflict).safe_strict():
            return True
        if self.excluding(conflict + 1).safe_strict():
            return True
        inverted = self.inverted()
        conflict = inverted.conflict()
        if conflict is None:
            return True
        if inverted.excluding(conflict).safe_strict():
            return True
        if inverted.excluding(conflict + 1).safe_strict():
            return True
        return False

    def safe_strict(self):
        """
        Determine whether this report is strictly safe.

        A report is strictly safe if all levels are strictly increasing
        or decreasing (this method checks increasing only), and
        consecutive levels are 1-3 apart, even without removing any
        level.
        """
        return all(
            1 <= (b - a) <= 3 for a, b in itertools.pairwise(self.levels)
        )

    def conflict(self):
        """
        Return the first index where a conflict occurs.

        If there is no conflict, return None.
        """
        for index in range(len(self.levels) - 1):
            a = self.levels[index]
            b = self.levels[index + 1]
            if 1 <= (b - a) <= 3:
                continue
            return index
        else:
            return None


levels = list(map(Report.from_input, stdin.readlines()))

n_safe = sum(level.safe() for level in levels)

print(n_safe)
