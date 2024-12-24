from sys import stdin


class Gate:

    def __init__(self, name: str):
        self.name = name
        self._formula = None

    def formula(self) -> str:
        pass


gates: dict[str, Gate] = {}


class StartingGate(Gate):

    def __init__(self, name: str, value: int):
        super().__init__(name)
        self._value = value

    @classmethod
    def from_input(self, data: str):
        name, value = data.split(": ")
        return StartingGate(name, int(value))

    def formula(self):
        return self.name


class AndGate(Gate):

    def __init__(self, name: str, a: str, b: str):
        super().__init__(name)
        self.a = a
        self.b = b

    @classmethod
    def from_input(self, data: str):
        inputs, name = data.split(" -> ")
        a, b = inputs.split(" AND ")
        return AndGate(name, a, b)

    def formula(self):
        if self.name.startswith("&") or self.name.startswith("^"):
            return self.name
        if self._formula is None:
            af = gates[self.a].formula()
            bf = gates[self.b].formula()
            if len(af) < len(bf):
                self._formula = f"AND ({af}, {bf})"
            else:
                self._formula = f"AND ({bf}, {af})"
        return self._formula


class OrGate(Gate):

    def __init__(self, name: str, a: str, b: str):
        super().__init__(name)
        self.a = a
        self.b = b

    @classmethod
    def from_input(self, data: str):
        inputs, name = data.split(" -> ")
        a, b = inputs.split(" OR ")
        return OrGate(name, a, b)

    def formula(self):
        if self.name.startswith("&") or self.name.startswith("^"):
            return self.name
        if self._formula is None:
            af = gates[self.a].formula()
            bf = gates[self.b].formula()
            if len(af) < len(bf):
                self._formula = f"OR ({af}, {bf})"
            else:
                self._formula = f"OR ({bf}, {af})"
        return self._formula


class XorGate(Gate):

    def __init__(self, name: str, a: str, b: str):
        super().__init__(name)
        self.a = a
        self.b = b

    @classmethod
    def from_input(self, data: str):
        inputs, name = data.split(" -> ")
        a, b = inputs.split(" XOR ")
        return XorGate(name, a, b)

    def formula(self):
        if self.name.startswith("&") or self.name.startswith("^"):
            return self.name
        if self._formula is None:
            af = gates[self.a].formula()
            bf = gates[self.b].formula()
            if len(af) < len(bf):
                self._formula = f"XOR ({af}, {bf})"
            else:
                self._formula = f"XOR ({bf}, {af})"
        return self._formula


def connecting_gate(data: str):
    if " AND " in data:
        return AndGate.from_input(data)
    elif " OR " in data:
        return OrGate.from_input(data)
    elif " XOR " in data:
        return XorGate.from_input(data)


starting_part, connecting_part = stdin.read().split("\n\n")
starting_gates = [
    StartingGate.from_input(gate) for gate in starting_part.splitlines()
]
connecting_gates = [
    connecting_gate(gate) for gate in connecting_part.splitlines()
]
gates = {gate.name: gate for gate in starting_gates + connecting_gates}

for name in sorted(gates):
    print(f"{name} = {gates[name].formula()}")


# There is supposed to be a pattern to the formulae of each output gate.
# The 4 swaps can be identified by looking for flaws in the pattern that
# this code initially outputs.
