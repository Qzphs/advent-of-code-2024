from enum import Enum
import itertools
from sys import stdin


# Keeping this solution merely to preserve the original attempt. 21h.py
# cleanly solves both Part One and Part Two of the problem.


class Key(Enum):

    A = "A"
    UP = "^"
    LEFT = "<"
    DOWN = "v"
    RIGHT = ">"


"""
Keypad cost lookup table.

`controller_costs[origin][destination]` gives the total number of human
keypresses needed to move from `origin` to `destination`, then press
`destination`.

This table was manually calculated for the keypad directly controlling
the numeric keypad.
"""
keypad_costs = {
    Key.A: {Key.A: 1, Key.UP: 8, Key.LEFT: 10, Key.DOWN: 9, Key.RIGHT: 6},
    Key.UP: {Key.A: 4, Key.UP: 1, Key.LEFT: 9, Key.DOWN: 6, Key.RIGHT: 7},
    Key.LEFT: {Key.A: 8, Key.UP: 7, Key.LEFT: 1, Key.DOWN: 4, Key.RIGHT: 5},
    Key.DOWN: {Key.A: 7, Key.UP: 4, Key.LEFT: 8, Key.DOWN: 1, Key.RIGHT: 4},
    Key.RIGHT: {Key.A: 4, Key.UP: 9, Key.LEFT: 9, Key.DOWN: 8, Key.RIGHT: 1},
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


def keypad_cost(sequence: tuple[Key]):
    return sum(
        keypad_costs[origin][destination]
        for origin, destination in itertools.pairwise(
            (Key.A,) + sequence + (Key.A,)
        )
    )


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

        result += min(keypad_cost(sequence) for sequence in sequences)

    return result


print(
    sum(
        int(code[:-1]) * best_keypad_cost(code)
        for code in stdin.read().splitlines()
    )
)
