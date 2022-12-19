import pathlib


def parse(input: str):
    lines = input.splitlines()
    rucksacks = []
    for line in lines:
        n = len(line)
        rucksacks.append((line[:n // 2], line[n // 2:]))
    return rucksacks


def to_priority(c: str):
    assert len(c) == 1
    alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet_lower = alphabet_upper.lower()
    if c in alphabet_lower:
        return alphabet_lower.index(c) + 1
    assert c in alphabet_upper
    return alphabet_upper.index(c) + 27


def part1(input: str):
    rucksacks = parse(input)
    result = 0
    for a, b in rucksacks:
        both = set(a) & set(b)
        result += sum(map(to_priority, both))
    return result


def test_part1():
    input = pathlib.Path("data/input-03-test.txt").read_text()
    assert part1(input) == 157

    input = pathlib.Path("data/input-03-real.txt").read_text()
    assert part1(input) == 7674


def part2(input: str):
    rucksacks = input.splitlines()
    result = 0
    for group in range(len(rucksacks) // 3):
        a, b, c = rucksacks[group * 3], rucksacks[group * 3 + 1], rucksacks[group * 3 + 2]
        common = set(a) & set(b) & set(c)
        item = list(common)[0]
        result += to_priority(item)
    return result


def test_part2():
    input = pathlib.Path("data/input-03-test.txt").read_text()
    assert part2(input) == 70

    input = pathlib.Path("data/input-03-real.txt").read_text()
    assert part2(input) == 2805
