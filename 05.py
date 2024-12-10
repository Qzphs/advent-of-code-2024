from sys import stdin


class Rule:

    def __init__(self, before: int, after: int):
        self.before = before
        self.after = after

    @classmethod
    def from_input(cls, data: str):
        before, after = map(int, data.split("|"))
        return Rule(before, after)


class Update:

    def __init__(self, pages: list[int]):
        self.indices = [None] * (max(pages) + 1)
        self.middle = pages[len(pages) // 2]
        for index, page in enumerate(pages):
            self.indices[page] = index

    @classmethod
    def from_input(cls, data: str):
        pages = [int(page) for page in data.split(",")]
        return Update(pages)

    def index(self, page: int):
        if not 0 <= page < len(self.indices):
            return None
        return self.indices[page]

    def correct(self, rules: list[Rule]):
        return all(self.follows(rule) for rule in rules)

    def follows(self, rule: Rule):
        before_index = self.index(rule.before)
        after_index = self.index(rule.after)
        if before_index is None or after_index is None:
            return True
        return before_index <= after_index


rules_data, updates_data = stdin.read().split("\n\n")
rules = [Rule.from_input(rule) for rule in rules_data.splitlines()]
updates = [Update.from_input(update) for update in updates_data.splitlines()]
print(sum(update.middle for update in updates if update.correct(rules)))
