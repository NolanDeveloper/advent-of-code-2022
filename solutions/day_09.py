import pathlib
import numpy as np


def part1(text: str):
    lines = text.splitlines()
    head_position = np.array([0, 0])
    tail_position = np.array([0, 0])
    visited = {tuple(tail_position)}
    for line in lines:
        direction, distance = line.split()
        distance = int(distance)
        offset = {
            'U': (0, 1),
            'R': (1, 0),
            'D': (0, -1),
            'L': (-1, 0),
        }[direction]
        for _ in range(distance):
            head_position += offset
            if np.any(np.abs(head_position - tail_position) >= 2):
                tail_position += np.sign(head_position - tail_position)
            visited.add(tuple(tail_position))
    return len(visited)


def part2(text: str):
    lines = text.splitlines()
    rope = [np.array([0, 0]) for _ in range(10)]
    visited = {(0, 0)}
    for line in lines:
        direction, distance = line.split()
        distance = int(distance)
        offset = {
            'U': (0, 1),
            'R': (1, 0),
            'D': (0, -1),
            'L': (-1, 0),
        }[direction]
        for _ in range(distance):
            rope[0] += offset
            for i in range(1, 10):
                if np.any(np.abs(rope[i] - rope[i - 1]) >= 2):
                    rope[i] += np.sign(rope[i - 1] - rope[i])
            visited.add(tuple(rope[9]))
    return len(visited)


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    test_big_text = pathlib.Path(f"data/input-{day:02}-test-big.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 13
    assert part1(real_text) == 6464
    assert part2(test_big_text) == 36
    assert part2(real_text) == 2604
