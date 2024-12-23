import itertools
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

    def groups(self):
        result = []
        for host in self.computers:
            if not host.startswith("t"):
                continue
            for a, b in itertools.combinations(self.computers[host], 2):
                if a.startswith("t") and a < host:
                    continue
                if b.startswith("t") and b < host:
                    continue
                if a in self.computers[b]:
                    result.append((host, a, b))
        return result


network = Network.from_input(stdin.read())
print(len(network.groups()))

# 0.003s
