from enum import Enum
import itertools
from sys import stdin


class Key(Enum):

    A = 0
    LEFT = 1
    UP = 2
    DOWN = 3
    RIGHT = 4

    @property
    def index(self):
        return self.value


class Keypad:

    def __init__(self):
        self.costs = [1] * (len(Key) * len(Key))

    @classmethod
    def nested(self, n: int):
        keypad = Keypad()
        for _ in range(n):
            keypad = keypad.nest()
        return keypad

    def get(self, start: Key, target: Key):
        return self.costs[(start.index * 5) + target.index]

    def set(self, start: Key, target: Key, cost: int):
        self.costs[(start.index * 5) + target.index] = cost

    def nest(self):
        nested = Keypad()
        nested.set(
            Key.A,
            Key.LEFT,
            min(
                self.get(Key.A, Key.LEFT)
                + self.get(Key.LEFT, Key.DOWN)
                + self.get(Key.DOWN, Key.LEFT)
                + self.get(Key.LEFT, Key.A),
                self.get(Key.A, Key.DOWN)
                + self.get(Key.DOWN, Key.LEFT)
                + self.get(Key.LEFT, Key.LEFT)
                + self.get(Key.LEFT, Key.A),
            ),
        )
        nested.set(
            Key.A,
            Key.UP,
            self.get(Key.A, Key.LEFT) + self.get(Key.LEFT, Key.A),
        )
        nested.set(
            Key.A,
            Key.DOWN,
            min(
                self.get(Key.A, Key.LEFT)
                + self.get(Key.LEFT, Key.DOWN)
                + self.get(Key.DOWN, Key.A),
                self.get(Key.A, Key.DOWN)
                + self.get(Key.DOWN, Key.LEFT)
                + self.get(Key.LEFT, Key.A),
            ),
        )
        nested.set(
            Key.A,
            Key.RIGHT,
            self.get(Key.A, Key.DOWN) + self.get(Key.DOWN, Key.A),
        )
        nested.set(
            Key.LEFT,
            Key.A,
            min(
                self.get(Key.A, Key.RIGHT)
                + self.get(Key.RIGHT, Key.RIGHT)
                + self.get(Key.RIGHT, Key.UP)
                + self.get(Key.UP, Key.A),
                self.get(Key.A, Key.RIGHT)
                + self.get(Key.RIGHT, Key.UP)
                + self.get(Key.UP, Key.RIGHT)
                + self.get(Key.RIGHT, Key.A),
            ),
        )
        nested.set(
            Key.LEFT,
            Key.UP,
            self.get(Key.A, Key.RIGHT)
            + self.get(Key.RIGHT, Key.UP)
            + self.get(Key.UP, Key.A),
        )
        nested.set(
            Key.LEFT,
            Key.DOWN,
            self.get(Key.A, Key.RIGHT) + self.get(Key.RIGHT, Key.A),
        )
        nested.set(
            Key.LEFT,
            Key.RIGHT,
            self.get(Key.A, Key.RIGHT)
            + self.get(Key.RIGHT, Key.RIGHT)
            + self.get(Key.RIGHT, Key.A),
        )
        nested.set(
            Key.UP,
            Key.A,
            self.get(Key.A, Key.RIGHT) + self.get(Key.RIGHT, Key.A),
        )
        nested.set(
            Key.UP,
            Key.LEFT,
            self.get(Key.A, Key.DOWN)
            + self.get(Key.DOWN, Key.LEFT)
            + self.get(Key.LEFT, Key.A),
        )
        nested.set(
            Key.UP,
            Key.DOWN,
            self.get(Key.A, Key.DOWN) + self.get(Key.DOWN, Key.A),
        )
        nested.set(
            Key.UP,
            Key.RIGHT,
            min(
                self.get(Key.A, Key.RIGHT)
                + self.get(Key.RIGHT, Key.DOWN)
                + self.get(Key.DOWN, Key.A),
                self.get(Key.A, Key.DOWN)
                + self.get(Key.DOWN, Key.RIGHT)
                + self.get(Key.RIGHT, Key.A),
            ),
        )
        nested.set(
            Key.DOWN,
            Key.A,
            min(
                self.get(Key.A, Key.RIGHT)
                + self.get(Key.RIGHT, Key.UP)
                + self.get(Key.UP, Key.A),
                self.get(Key.A, Key.UP)
                + self.get(Key.UP, Key.RIGHT)
                + self.get(Key.RIGHT, Key.A),
            ),
        )
        nested.set(
            Key.DOWN,
            Key.LEFT,
            self.get(Key.A, Key.LEFT) + self.get(Key.LEFT, Key.A),
        )
        nested.set(
            Key.DOWN,
            Key.UP,
            self.get(Key.A, Key.UP) + self.get(Key.UP, Key.A),
        )
        nested.set(
            Key.DOWN,
            Key.RIGHT,
            self.get(Key.A, Key.RIGHT) + self.get(Key.RIGHT, Key.A),
        )
        nested.set(
            Key.RIGHT,
            Key.A,
            self.get(Key.A, Key.UP) + self.get(Key.UP, Key.A),
        )
        nested.set(
            Key.RIGHT,
            Key.LEFT,
            self.get(Key.A, Key.LEFT)
            + self.get(Key.LEFT, Key.LEFT)
            + self.get(Key.LEFT, Key.A),
        )
        nested.set(
            Key.RIGHT,
            Key.UP,
            min(
                self.get(Key.A, Key.LEFT)
                + self.get(Key.LEFT, Key.UP)
                + self.get(Key.UP, Key.A),
                self.get(Key.A, Key.UP)
                + self.get(Key.UP, Key.LEFT)
                + self.get(Key.LEFT, Key.A),
            ),
        )
        nested.set(
            Key.RIGHT,
            Key.DOWN,
            self.get(Key.A, Key.LEFT) + self.get(Key.LEFT, Key.A),
        )
        return nested


final_robot_keypad = Keypad.nested(25)


coordinates = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}


def possible_sequences(du: int, dv: int):
    """
    Return a set of sequences that move by (du, dv).

    Sequences always start from A and omit the final A press.
    """
    if du == 0 and dv == 0:
        return {tuple()}
    if du == 0 and dv < 0:
        return {(Key.LEFT,) * -dv}
    if du == 0 and dv > 0:
        return {(Key.RIGHT,) * dv}
    if du < 0 and dv == 0:
        return {(Key.UP,) * -du}
    if du > 0 and dv == 0:
        return {(Key.DOWN,) * du}
    assert du != 0 and dv != 0
    u_key = Key.UP if du < 0 else Key.DOWN
    v_key = Key.LEFT if dv < 0 else Key.RIGHT
    return set(
        itertools.permutations(
            ([u_key] * abs(du)) + ([v_key] * abs(dv)), r=abs(du) + abs(dv)
        )
    )


def numeric_cost(sequence: tuple[Key]):
    return sum(
        final_robot_keypad.get(origin, destination)
        for origin, destination in itertools.pairwise(
            (Key.A,) + sequence + (Key.A,)
        )
    )




def best_keypad_cost(code: str):
    result = 0
    for origin, destination in itertools.pairwise("A" + code):
        u0, v0 = coordinates[origin]
        u1, v1 = coordinates[destination]
        du = u1 - u0
        dv = v1 - v0

        sequences = possible_sequences(du, dv)

        if origin == "A" and destination == "1":
            sequences.remove((Key.LEFT, Key.LEFT, Key.UP))
        elif origin == "A" and destination == "4":
            sequences.remove((Key.LEFT, Key.LEFT, Key.UP, Key.UP))
        elif origin == "A" and destination == "7":
            sequences.remove((Key.LEFT, Key.LEFT, Key.UP, Key.UP, Key.UP))
        elif origin == "0" and destination == "1":
            sequences.remove((Key.LEFT, Key.UP))
        elif origin == "0" and destination == "4":
            sequences.remove((Key.LEFT, Key.UP, Key.UP))
        elif origin == "0" and destination == "7":
            sequences.remove((Key.LEFT, Key.UP, Key.UP, Key.UP))

        elif origin == "1" and destination == "A":
            sequences.remove((Key.DOWN, Key.RIGHT, Key.RIGHT))
        elif origin == "4" and destination == "A":
            sequences.remove((Key.DOWN, Key.DOWN, Key.RIGHT, Key.RIGHT))
        elif origin == "7" and destination == "A":
            sequences.remove(
                (Key.DOWN, Key.DOWN, Key.DOWN, Key.RIGHT, Key.RIGHT)
            )
        elif origin == "1" and destination == "0":
            sequences.remove((Key.DOWN, Key.RIGHT))
        elif origin == "4" and destination == "0":
            sequences.remove((Key.DOWN, Key.DOWN, Key.RIGHT))
        elif origin == "7" and destination == "0":
            sequences.remove((Key.DOWN, Key.DOWN, Key.DOWN, Key.RIGHT))

        result += min(numeric_cost(sequence) for sequence in sequences)

    return result


print(
    sum(
        int(code[:-1]) * best_keypad_cost(code)
        for code in stdin.read().splitlines()
    )
)
