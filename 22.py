from sys import stdin


class Secret:

    def __init__(self, number: int):
        self.number = number

    def evolve(self):
        self.mix(self.number * 64)
        self.prune()
        self.mix(round(self.number // 32))
        self.prune()
        self.mix(self.number * 2048)
        self.prune()

    def mix(self, value: int):
        self.number = self.number ^ value

    def prune(self):
        self.number = self.number % 16777216


final_sum = 0
for number in stdin.read().splitlines():
    secret = Secret(int(number))
    for _ in range(2000):
        secret.evolve()
    final_sum += secret.number
print(final_sum)
