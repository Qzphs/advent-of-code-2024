import itertools
from sys import stdin


# Both rules and updates in the actual input use the same set of 49
# distinct two-digit page numbers. Every pair of page numbers has a
# relationship somewhere within the rules. It's not possible for all
# rules to be simultaneously enforced, but presumably it is for the
# subsets used in each update. We'll use these observations to our
# advantage for Part Two.


class Rules:

    ADJMATRIX = [[None] * 100 for _ in range(100)]

    @classmethod
    def add(cls, before: int, after: int):
        cls.ADJMATRIX[before][after] = True
        cls.ADJMATRIX[after][before] = False

    @classmethod
    def query(cls, before: int, after: int):
        assert cls.ADJMATRIX[before][after] is not None
        return cls.ADJMATRIX[before][after]


class Update:

    def __init__(self, pages: list[int]):
        self.pages = pages

    @classmethod
    def from_input(cls, data: str):
        pages = [int(page) for page in data.split(",")]
        return Update(pages)

    def middle(self):
        """Return the middle page."""
        return self.pages[len(self.pages) // 2]

    def correct(self):
        """Determine whether pages are sorted."""
        return all(
            Rules.query(before, after)
            for before, after in itertools.pairwise(self.pages)
        )

    def ordered(self):
        """Return a copy with pages sorted using rules."""
        original = Update(self.pages)
        result = []
        while original.pages:
            result.append(original.reduce())
        return Update(result)

    def reduce(self):
        """Find, remove, and return the minimum page."""
        for page in self.pages:
            if any(
                Rules.query(other, page)
                for other in self.pages
                if other != page
            ):
                continue
            self.pages.remove(page)
            return page
        assert False, "no minimum"


rules, updates_data = stdin.read().split("\n\n")
for rule in rules.splitlines():
    before, after = map(int, rule.split("|"))
    Rules.add(before, after)
updates = [Update.from_input(update) for update in updates_data.splitlines()]
print(
    sum(
        update.ordered().middle() for update in updates if not update.correct()
    )
)
