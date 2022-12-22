import pathlib
import numpy as np


def add_rock(grid: dict[(int, int), str], a: (int, int), b: (int, int)):
    x1, y1 = a
    x2, y2 = b
    dx = np.sign(x2 - x1)
    dy = np.sign(y2 - y1)
    x, y = x1, y1
    while x != x2 or y != y2:
        grid[(x, y)] = '#'
        x += dx
        y += dy
    grid[(x, y)] = '#'


def parse(text: str):
    grid = {}
    for line in text.splitlines():
        coordinates = []
        for coordinate in line.split(" -> "):
            x, y = coordinate.split(",")
            coordinates.append((int(x), int(y)))
        for i in range(len(coordinates) - 1):
            add_rock(grid, coordinates[i], coordinates[i + 1])
    return grid


def print_grid(grid: dict[(int, int), str]):
    left = min(x for x, _ in grid.keys())
    right = max(x for x, _ in grid.keys())
    top = min(y for _, y in grid.keys())
    bottom = max(y for _, y in grid.keys())
    print()
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if (x, y) in grid:
                block = grid[(x, y)]
            else:
                block = ' '
            print(block, end='')
        print()


def peek_greed(grid: dict[(int, int), str], x: int, y: int) -> str:
    if (x, y) in grid:
        return grid[(x, y)]
    return ' '


def part1(text: str):
    grid = parse(text)
    bottom = max(y for _, y in grid.keys())
    source = (500, 0)
    amount_of_sand = 0
    overflow = False
    while not overflow:
        x, y = source
        while True:
            if y > bottom:
                overflow = True
                break
            if peek_greed(grid, x, y + 1) == ' ':
                y += 1
                continue
            if peek_greed(grid, x - 1, y + 1) == ' ':
                y += 1
                x -= 1
                continue
            if peek_greed(grid, x + 1, y + 1) == ' ':
                y += 1
                x += 1
                continue
            break
        grid[(x, y)] = 'O'
        amount_of_sand += 1
    return amount_of_sand - 1


def peek_greed_with_floor(grid: dict[(int, int), str], x: int, y: int, floor_level: int) -> str:
    if y >= floor_level:
        return '#'
    if (x, y) in grid:
        return grid[(x, y)]
    return ' '


def part2(text: str):
    grid = parse(text)
    floor_level = 2 + max(y for _, y in grid.keys())
    source = (500, 0)
    amount_of_sand = 0
    while True:
        x, y = source
        while True:
            if peek_greed_with_floor(grid, x, y + 1, floor_level) == ' ':
                y += 1
                continue
            if peek_greed_with_floor(grid, x - 1, y + 1, floor_level) == ' ':
                y += 1
                x -= 1
                continue
            if peek_greed_with_floor(grid, x + 1, y + 1, floor_level) == ' ':
                y += 1
                x += 1
                continue
            break
        if (x, y) == source:
            break
        grid[(x, y)] = 'O'
        amount_of_sand += 1
    return amount_of_sand + 1


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 24
    assert part1(real_text) == 644
    assert part2(test_text) == 93
    assert part2(real_text) == 27324
