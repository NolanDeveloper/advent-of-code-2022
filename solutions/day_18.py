import operator
import pathlib
from collections import deque


def parse(text: str):
    cubes = []
    for line in text.splitlines():
        cubes.append(tuple(int(x) for x in line.split(',')))
    return cubes


def zip_with(f, a, b):
    assert len(a) == len(b)
    return tuple(f(a[i], b[i]) for i in range(len(a)))


def is_in_box(box, cell):
    return all(zip_with(operator.le, box[0], cell)) and all(zip_with(operator.le, cell, box[1]))


def part1(text: str):
    cubes = parse(text)
    displacements = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    potential_shell = [
        zip_with(operator.add, cube, displacement)
        for cube in cubes
        for displacement in displacements
    ]
    shell = [
        cube
        for cube in potential_shell
        if cube not in cubes
    ]
    return len(shell)


def part2(text: str):
    cubes = set(parse(text))
    displacements = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    some_cube = next(iter(cubes))
    bounding_box = [some_cube, some_cube]
    for cube in cubes:
        bounding_box[0] = zip_with(min, bounding_box[0], cube)
        bounding_box[1] = zip_with(max, bounding_box[1], cube)
    bounding_box[0] = zip_with(operator.sub, bounding_box[0], (1, 1, 1))
    bounding_box[1] = zip_with(operator.add, bounding_box[1], (1, 1, 1))
    outside = set()
    queue = deque()
    queue.append(bounding_box[0])
    while queue:
        cell = queue.pop()
        if cell in cubes or cell in outside or not is_in_box(bounding_box, cell):
            continue
        outside.add(cell)
        for displacement in displacements:
            queue.append(zip_with(operator.add, cell, displacement))
    potential_shell = [
        zip_with(operator.add, cube, displacement)
        for cube in cubes
        for displacement in displacements
    ]
    shell = [
        cube
        for cube in potential_shell
        if cube in outside
    ]
    return len(shell)


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1('1,1,1\n2,1,1\n') == 10
    assert part1(test_text) == 64
    assert part1(real_text) == 4418
    assert part2(test_text) == 58
    assert part2(real_text) == 2486
