from sys import stdin


class Gate:

    def __init__(self, name: str):
        self.name = name
        self._value = None

    def value(self):
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

    def value(self):
        return self._value


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

    def value(self):
        if self._value is None:
            self._value = gates[self.a].value() & gates[self.b].value()
        return self._value


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

    def value(self):
        if self._value is None:
            self._value = gates[self.a].value() | gates[self.b].value()
        return self._value


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

    def value(self):
        if self._value is None:
            self._value = gates[self.a].value() ^ gates[self.b].value()
        return self._value


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

z_gates = (gates[name] for name in sorted(gates) if name.startswith("z"))
z_values = [gate.value() for gate in z_gates]
print(sum(value << i for i, value in enumerate(z_values)))
