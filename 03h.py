from sys import stdin


class Instruction:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"mul({self.x},{self.y})"

    def product(self):
        return self.x * self.y


class Program:

    def __init__(self, memory: str):
        self.memory = memory

    def instructions(self):
        """Find all valid instructions in the memory."""
        instructions: list[Instruction] = []
        enabled = True
        for index, _ in enumerate(self.memory):
            if self.memory[index:index+4] == "do()":
                enabled = True
                continue
            if self.memory[index:index+7] == "don't()":
                enabled = False
                continue
            if not enabled:
                continue
            instruction = self._instruction_at(index)
            if instruction is None:
                continue
            instructions.append(instruction)
        return instructions

    def _instruction_at(self, index: int):
        """
        Decode instruction using memory from `index` onwards.

        Return the decoded instruction.

        If the memory from `index` onwards does not represent a valid
        instruction, return None instead.
        """
        if self.memory[index : index + 4] != "mul(":
            return None
        x_start = index + 4
        x_end = self.memory.find(",", x_start)
        if x_end == -1:
            return None
        if x_end - x_start > 3:
            return None
        if not self.memory[x_start:x_end].isdigit():
            return None
        y_start = x_end + 1
        y_end = self.memory.find(")", y_start)
        if y_end == -1:
            return None
        if y_end - y_start > 3:
            return None
        if not self.memory[y_start:y_end].isdigit():
            return None
        return Instruction(
            int(self.memory[x_start:x_end]), int(self.memory[y_start:y_end])
        )


program = Program(stdin.read())

instructions = program.instructions()

print(sum(instruction.product() for instruction in instructions))
