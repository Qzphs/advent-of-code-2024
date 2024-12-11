class StoneCollection:

    def __init__(self):
        self.stones: dict[str, int] = {}

    @classmethod
    def from_input(cls, data: str):
        result = StoneCollection()
        for stone in data.split():
            result.add(stone, 1)
        return result

    def add(self, stone: str, amount: int):
        if stone not in self.stones:
            self.stones[stone] = 0
        self.stones[stone] += amount

    def blink(self):
        result = StoneCollection()
        for stone, amount in self.stones.items():
            if stone == "0":
                result.add("1", amount)
            elif len(stone) % 2 == 0:
                left = str(int(stone[: len(stone) // 2]))
                right = str(int(stone[len(stone) // 2 :]))
                result.add(left, amount)
                result.add(right, amount)
            else:
                multiplied = str(int(stone) * 2024)
                result.add(multiplied, amount)
        return result

    def total(self):
        return sum(self.stones.values())


stones = StoneCollection.from_input(input())
for _ in range(75):
    stones = stones.blink()
print(stones.total())
