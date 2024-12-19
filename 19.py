from sys import stdin


patterns = input().split(", ")
input()  # For the blank line


def possible(design: str):
    for pattern in patterns:
        if not design.startswith(pattern):
            continue
        if design == pattern:
            return True
        if possible(design.removeprefix(pattern)):
            return True
    return False


designs = stdin.read().splitlines()
print(sum(1 for design in designs if possible(design)))
