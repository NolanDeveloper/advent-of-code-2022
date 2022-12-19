import pathlib


def parse_range(input: str) -> (int, int):
    a, b = input.split("-")
    return int(a), int(b)


def parse(input: str) -> list[tuple[(int, int), (int, int)]]:
    ranges = []
    for line in input.splitlines():
        first, second = line.split(",")
        pair = parse_range(first), parse_range(second)
        ranges.append(pair)
    return ranges


def intersect(a: (int, int), b: (int, int)) -> (int, int):
    return max(a[0], b[0]), min(a[1], b[1])


def part1(input: str):
    ranges = parse(input)
    result = 0
    for first, second in ranges:
        intersection = intersect(first, second)
        if intersection in [first, second]:
            result += 1
    return result


def test_part1():
    input = pathlib.Path("data/input-04-test.txt").read_text()
    assert part1(input) == 2

    input = pathlib.Path("data/input-04-real.txt").read_text()
    assert part1(input) == 444


def part2(input: str):
    ranges = parse(input)
    result = 0
    for first, second in ranges:
        intersection = intersect(first, second)
        if intersection[0] <= intersection[1]:
            result += 1
    return result


def test_part2():
    input = pathlib.Path("data/input-04-test.txt").read_text()
    assert part2(input) == 4

    input = pathlib.Path("data/input-04-real.txt").read_text()
    assert part2(input) == 801
