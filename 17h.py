from collections import deque
from sys import stdin


class Computer:

    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.pointer = 0
        self.output = []

    @classmethod
    def from_input(cls, data: str):
        a_part, b_part, c_part, _, input_part = data.splitlines()
        computer = Computer(
            int(a_part.removeprefix("Register A: ")),
            int(b_part.removeprefix("Register B: ")),
            int(c_part.removeprefix("Register C: ")),
            list(map(int, input_part.removeprefix("Program: ").split(","))),
        )
        return computer

    def run(self):
        while 0 <= self.pointer < len(self.program) - 1:
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer + 1]
            self.pointer += 2
            self.execute(opcode, operand)

    def execute(self, opcode: int, operand: int):
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)
        elif opcode == 4:
            self.bxc(operand)
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)

    def combo(self, operand: int):
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        return operand

    def adv(self, operand: int):
        self.a = self.a // (2 ** self.combo(operand))

    def bxl(self, operand: int):
        self.b = self.b ^ operand

    def bst(self, operand: int):
        self.b = self.combo(operand) % 8

    def jnz(self, operand: int):
        if self.a == 0:
            return
        self.pointer = operand

    def bxc(self, operand: int):
        self.b = self.b ^ self.c

    def out(self, operand: int):
        self.output.append(self.combo(operand) % 8)

    def bdv(self, operand: int):
        self.b = self.a // (2 ** self.combo(operand))

    def cdv(self, operand: int):
        self.c = self.a // (2 ** self.combo(operand))

    def viable(self):
        """
        Determine whether this computer is viable.

        This computer is viable if its output matches the final however
        many bits of its program.
        """
        program_string = ",".join(str(number) for number in self.program)
        output_string = ",".join(str(number) for number in self.output)
        return program_string.endswith(output_string)


test1 = Computer(0, 0, 9, [2, 6])
test1.run()
assert test1.b == 1

test2 = Computer(10, 0, 0, [5, 0, 5, 1, 5, 4])
test2.run()
assert test2.output == [0, 1, 2]

test3 = Computer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
test3.run()
assert test3.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
assert test3.a == 0

test4 = Computer(0, 29, 0, [1, 7])
test4.run()
assert test4.b == 26

test5 = Computer(0, 2024, 43690, [4, 0])
test5.run()
assert test5.b == 44354


# The program seems to loop through the A register 3 bits at a time.
# These batches of bits are independent of each other, so we can build
# the input batch by batch.


def build_input():
    original = Computer.from_input(stdin.read())
    parts: deque[int] = deque()
    parts.append(0)
    while parts:
        part = parts.popleft()
        for suffix in range(8):
            a = (part << 3) + suffix
            copy = Computer(a, original.b, original.c, original.program.copy())
            copy.run()
            if copy.output == copy.program:
                return a
            if not copy.viable():
                continue
            parts.append(a)


print(build_input())
