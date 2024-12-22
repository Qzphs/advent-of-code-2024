from collections import deque
from sys import stdin


def evolve(secret):
    secret = (secret ^ (secret << 6)) & 16777215
    secret = (secret ^ (secret >> 5)) & 16777215
    secret = (secret ^ (secret << 11)) & 16777215
    return secret


class Seller:

    def __init__(self, initial: int):
        self.purchases = {}
        changes = deque(maxlen=4)
        old_secret = initial
        old_price = old_secret % 10
        for _ in range(3):
            new_secret = evolve(old_secret)
            new_price = new_secret % 10
            changes.append(new_price - old_price)
            old_secret = new_secret
            old_price = new_price
        for _ in range(1997):
            new_secret = evolve(old_secret)
            new_price = new_secret % 10
            changes.append(new_price - old_price)
            if tuple(changes) not in self.purchases:
                self.purchases[tuple(changes)] = new_price
            old_secret = new_secret
            old_price = new_price

    def sequences(self):
        return self.purchases.keys()

    def purchase(self, sequence: tuple[int, int, int, int]):
        if sequence not in self.purchases:
            return 0
        return self.purchases[sequence]


sellers = [Seller(secret0) for secret0 in map(int, stdin.read().splitlines())]
sequences = set()
sequences.update(*(seller.sequences() for seller in sellers))
print(
    max(
        sum(seller.purchase(sequence) for seller in sellers)
        for sequence in sequences
    )
)

# Running time: 13.3s
