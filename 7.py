from sys import stdin


class Equation:

    def __init__(self, test_value: int, operands: list[int]):
        self.test_value = test_value
        self.operands = operands

    @classmethod
    def from_input(cls, data: str):
        left, right = data.split(": ")
        return Equation(int(left), [int(operand) for operand in right.split()])

    def without_last_added(self):
        return Equation(
            self.test_value - self.operands[-1], self.operands[:-1]
        )

    def without_last_multiplied(self):
        return Equation(
            self.test_value // self.operands[-1], self.operands[:-1]
        )

    def possibly_true(self):
        if len(self.operands) == 1:
            return self.test_value == self.operands[0]
        if self.test_value % self.operands[-1] != 0:
            return self.without_last_added().possibly_true()
        return (
            self.without_last_added().possibly_true()
            or self.without_last_multiplied().possibly_true()
        )


equations = [Equation.from_input(equation) for equation in stdin.readlines()]
print(
    sum(
        equation.test_value
        for equation in equations
        if equation.possibly_true()
    )
)
