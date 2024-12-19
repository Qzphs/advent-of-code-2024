import itertools
from sys import stdin


patterns = sorted(input().split(", "))
input()  # For the blank line


def arrangements_small(small: str):
    n = 0
    for pattern in patterns:
        if not small.startswith(pattern):
            continue
        if small == pattern:
            n += 1
        n += arrangements_small(small.removeprefix(pattern))
    return n


small_length = 5
smalls = sum(
    (
        [
            "".join(colours)
            for colours in itertools.product("bgruw", repeat=length)
        ]
        for length in range(small_length + 1)
    ),
    start=[],
)
small_arrangements = {
    small: arrangements_small("".join(small)) for small in smalls
}
small_arrangements[""] = 1


def arrangements_large(large: str):
    if len(large) <= small_length:
        return small_arrangements[large]
    target = len(large) // 2
    n = arrangements_large(large[:target]) * arrangements_large(large[target:])
    for start in range(target - 7, target):
        for pattern in patterns:
            if start + len(pattern) <= target:
                continue
            if large[start : start + len(pattern)] != pattern:
                continue
            n += arrangements_large(large[:start]) * arrangements_large(
                large[start + len(pattern) :]
            )
    return n


designs = stdin.read().splitlines()
print(sum(arrangements_large(design) for design in designs))
