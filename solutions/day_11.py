import math
import pathlib
from typing import Callable
from dataclasses import dataclass, field


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int] = field(repr=False)
    test_value: int = field()
    true_monkey: int = field()
    false_monkey: int = field()
    number_of_inspected_items: int = 0


def parse(text: str):
    monkeys = []
    for section in text.split("\n\n"):
        lines = section.splitlines()
        items = list(map(lambda s: int(s.removesuffix(',')), lines[1].split()[2:]))
        operation_sign = lines[2].split()[4]
        value = lines[2].split()[5]
        if operation_sign == '+':
            def operation(x: int, y: str = value) -> int:
                if y == 'old':
                    return x + x
                else:
                    return x + int(y)
        else:
            assert operation_sign == '*'

            def operation(x: int, y: str = value) -> int:
                if y == 'old':
                    return x * x
                else:
                    return x * int(y)
        test_value = int(lines[3].split()[3])
        true_monkey = int(lines[4].split()[5])
        false_monkey = int(lines[5].split()[5])
        monkeys.append(Monkey(items, operation, test_value, true_monkey, false_monkey))
    return monkeys


def part1(text: str):
    monkeys = parse(text)
    for _ in range(20):
        for i in range(len(monkeys)):
            monkeys[i].number_of_inspected_items += len(monkeys[i].items)
            for item in monkeys[i].items:
                new_worry_level = monkeys[i].operation(item) // 3
                if new_worry_level % monkeys[i].test_value == 0:
                    j = monkeys[i].true_monkey
                else:
                    j = monkeys[i].false_monkey
                monkeys[j].items.append(new_worry_level)
            monkeys[i].items = []
    activity = list(monkey.number_of_inspected_items for monkey in monkeys)
    activity.sort(reverse=True)
    return activity[0] * activity[1]


def part2(text: str):
    monkeys = parse(text)
    limit = math.prod(monkey.test_value for monkey in monkeys)
    for _ in range(10000):
        for i in range(len(monkeys)):
            monkeys[i].number_of_inspected_items += len(monkeys[i].items)
            for item in monkeys[i].items:
                new_worry_level = monkeys[i].operation(item) % limit
                if new_worry_level % monkeys[i].test_value == 0:
                    j = monkeys[i].true_monkey
                else:
                    j = monkeys[i].false_monkey
                monkeys[j].items.append(new_worry_level)
            monkeys[i].items = []
    activity = list(monkey.number_of_inspected_items for monkey in monkeys)
    activity.sort(reverse=True)
    return activity[0] * activity[1]


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 10605
    assert part1(real_text) == 99840
    assert part2(test_text) == 2713310158
    assert part2(real_text) == 20683044837
