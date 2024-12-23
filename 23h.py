from sys import stdin


class Network:

    def __init__(self):
        self.computers: dict[str, set[str]] = {}

    @classmethod
    def from_input(self, data: str):
        network = Network()
        for connection in data.splitlines():
            a, b = connection.split("-")
            network.add_connection(a, b)
        return network

    def add_connection(self, a: str, b: str):
        if a not in self.computers:
            self.computers[a] = set()
        if b not in self.computers:
            self.computers[b] = set()
        self.computers[a].add(b)
        self.computers[b].add(a)

    def connected(self, a: str, b: str):
        return a in self.computers[b]


# I couldn't be bothered binary searching, so I manually adjusted this
# constant while running multiple times

target = 13


def clique(current: list[str], remaining: list[str]):
    if len(current) == target:
        return current
    if not remaining:
        return None
    chosen = remaining[0]
    remaining_if_chosen = [
        computer
        for computer in remaining
        if network.connected(computer, chosen)
    ]
    return clique(current + [chosen], remaining_if_chosen) or clique(
        current, remaining[1:]
    )


network = Network.from_input(stdin.read())
print(",".join(sorted(clique([], list(network.computers)))))

# 0.1s
