from sys import stdin


class Machine:

    def __init__(self, ax: int, ay: int, bx: int, by: int, px: int, py: int):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px + 10000000000000
        self.py = py + 10000000000000

    @classmethod
    def from_input(cls, data: str):
        a_part, b_part, p_part = data.splitlines()
        ax, ay = map(int, a_part.removeprefix("Button A: X+").split(", Y+"))
        bx, by = map(int, b_part.removeprefix("Button B: X+").split(", Y+"))
        px, py = map(int, p_part.removeprefix("Prize: X=").split(", Y="))
        return Machine(ax, ay, bx, by, px, py)

    def tokens(self):
        a = self.a_presses()
        b = self.b_presses()
        x = a * self.ax + b * self.bx
        y = a * self.ay + b * self.by
        if (x, y) == (self.px, self.py):
            return (3 * a) + b
        else:
            return 0

    def a_presses(self):
        return round(
            (self.px - self.py * (self.bx / self.by))
            / (self.ax - self.ay * (self.bx / self.by))
        )

    def b_presses(self):
        return round(
            (self.px - self.py * (self.ax / self.ay))
            / (self.bx - self.by * (self.ax / self.ay))
        )


machines = [
    Machine.from_input(machine) for machine in stdin.read().split("\n\n")
]
print(sum(machine.tokens() for machine in machines))
