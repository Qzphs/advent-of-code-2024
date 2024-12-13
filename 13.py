from sys import stdin


class Machine:

    def __init__(
        self,
        ax: int,
        ay: int,
        bx: int,
        by: int,
        px: int,
        py: int,
    ):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

    @classmethod
    def from_input(cls, data: str):
        a_data, b_data, p_data = data.splitlines()
        ax, ay = map(int, a_data.removeprefix("Button A: X+").split(", Y+"))
        bx, by = map(int, b_data.removeprefix("Button B: X+").split(", Y+"))
        px, py = map(int, p_data.removeprefix("Prize: X=").split(", Y="))
        return Machine(ax, ay, bx, by, px, py)

    def cheapest_cost(self):
        """
        Calculate the cost of the cheapest winning combination.

        If the prize is not winnable, return 0 instead.
        """
        costs: list[int] = []
        for a in range(101):
            px = self.px - (a * self.ax)
            py = self.py - (a * self.ay)
            if px < 0:
                continue
            if py < 0:
                continue
            if px % self.bx != 0:
                continue
            if py % self.by != 0:
                continue
            if (px // self.bx) != (py // self.by):
                continue
            b = px // self.bx
            costs.append((3 * a) + b)
        if not costs:
            return 0
        return min(costs)


machines = [
    Machine.from_input(machine) for machine in stdin.read().split("\n\n")
]
print(sum(machine.cheapest_cost() for machine in machines))
