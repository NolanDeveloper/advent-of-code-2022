import pathlib
from typing import Union


def parse(text: str) -> dict[str, Union[int, tuple[str, str, str]]]:
    monkeys = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            name, value = parts
            monkeys[name[:-1]] = int(value)
        else:
            name, a, operation, b = parts
            monkeys[name[:-1]] = (a, operation, b)
    return monkeys


def part1(text: str):
    monkeys = parse(text)

    def calculate_value(name: str) -> int:
        if isinstance(monkeys[name], int):
            return monkeys[name]
        a, operation, b = monkeys[name]
        a = calculate_value(a)
        b = calculate_value(b)
        if operation == '+':
            monkeys[name] = a + b
        elif operation == '-':
            monkeys[name] = a - b
        elif operation == '*':
            monkeys[name] = a * b
        elif operation == '/':
            monkeys[name] = a // b
        return monkeys[name]

    return calculate_value('root')


def part2(text: str):
    monkeys = parse(text)
    unknowns = {}

    x, _, y = monkeys['root']

    def is_unknown(name: str) -> bool:
        if name in unknowns:
            return unknowns[name]
        if name == 'humn':
            return True
        if isinstance(monkeys[name], int):
            return False
        a, _, b = monkeys[name]
        return is_unknown(a) or is_unknown(b)

    def calculate_value(name: str) -> int:
        assert not is_unknown(name)
        if isinstance(monkeys[name], int):
            return monkeys[name]
        a, operation, b = monkeys[name]
        a = calculate_value(a)
        b = calculate_value(b)
        if operation == '+':
            monkeys[name] = a + b
        elif operation == '-':
            monkeys[name] = a - b
        elif operation == '*':
            monkeys[name] = a * b
        elif operation == '/':
            monkeys[name] = a // b
        return monkeys[name]

    def solve(name: str, value: int) -> int:
        if name == 'humn':
            return value
        a, operation, b = monkeys[name]
        assert is_unknown(a) or is_unknown(b)
        if operation == '/':
            if is_unknown(a):
                return solve(a, value * calculate_value(b))
            return solve(b, calculate_value(a) // value)
        elif operation == '-':
            if is_unknown(a):
                return solve(a, value + calculate_value(b))
            return solve(b, calculate_value(a) - value)
        else:
            if is_unknown(b):
                a, b = b, a
            if operation == '+':
                return solve(a, value - calculate_value(b))
            elif operation == '*':
                return solve(a, value // calculate_value(b))
        assert False

    if is_unknown(y):
        x, y = y, x
    return solve(x, calculate_value(y))


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 152
    assert part1(real_text) == 85616733059734
    assert part2(test_text) == 301
    assert part2(real_text) == 3560324848168
