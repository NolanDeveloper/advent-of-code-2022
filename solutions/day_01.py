import itertools
import pathlib


def parse(input):
    lines = input.splitlines()
    lines.append("")
    elves = []
    current_elf = []
    for line in lines:
        line = line.strip()
        if not line:
            elves.append(current_elf)
            current_elf = []
        else:
            current_elf.append(int(line))
    return elves


def part1(input):
    elves = parse(input)
    max_elf = max(elves, key=lambda x: sum(x))
    return sum(max_elf)


def test_part1():
    input = pathlib.Path("input-01-test.txt").read_text()
    assert part1(input) == 24000

    input = pathlib.Path("input-01-real.txt").read_text()
    assert part1(input) == 71124


def part2(input):
    elves = parse(input)
    elves = list(sorted(elves, reverse=True, key=lambda x: sum(x)))
    return sum(map(lambda x: sum(x), elves[:3]))


def test_part2():
    input = pathlib.Path("input-01-test.txt").read_text()
    assert part2(input) == 45000

    input = pathlib.Path("input-01-real.txt").read_text()
    assert part2(input) == 204639
