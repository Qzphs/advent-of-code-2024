from sys import stdin


class Equation:

    def __init__(self, test_value: int, operands: list[int]):
        self.test_value = test_value
        self.operands = operands

    @classmethod
    def from_input(cls, data: str):
        left, right = data.split(": ")
        return Equation(int(left), [int(operand) for operand in right.split()])

    def possibly_true(self):
        if len(self.operands) == 1:
            return self.test_value == self.operands[0]
        return (
            self._possibly_true_last_added()
            or self._possibly_true_last_multiplied()
            or self._possibly_true_last_concatenated()
        )

    def _possibly_true_last_added(self):
        if self.test_value < self.operands[-1]:
            return False
        child = Equation(
            self.test_value - self.operands[-1], self.operands[:-1]
        )
        return child.possibly_true()

    def _possibly_true_last_multiplied(self):
        if self.test_value % self.operands[-1] != 0:
            return False
        child = Equation(
            self.test_value // self.operands[-1], self.operands[:-1]
        )
        return child.possibly_true()

    def _possibly_true_last_concatenated(self):
        if self.test_value == self.operands[-1]:
            return False
        if not str(self.test_value).endswith(str(self.operands[-1])):
            return False
        child = Equation(
            int(str(self.test_value).removesuffix(str(self.operands[-1]))),
            self.operands[:-1],
        )
        return child.possibly_true()


equations = [Equation.from_input(equation) for equation in stdin.readlines()]
print(
    sum(
        equation.test_value
        for equation in equations
        if equation.possibly_true()
    )
)
