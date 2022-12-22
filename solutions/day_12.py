import pathlib
import queue as q
import numpy as np


def parse_height(char: str) -> int:
    if char == 'S':
        char = 'a'
    if char == 'E':
        char = 'z'
    return ord(char) - ord('a')


def parse(text: str):
    lines = text.splitlines()
    height, width = len(lines), len(lines[0].strip())
    heightmap = np.zeros((height, width))
    start_position = None
    end_position = None
    for row in range(height):
        for column in range(width):
            char = lines[row][column]
            if char == 'S':
                start_position = (row, column)
            if char == 'E':
                end_position = (row, column)
            heightmap[row, column] = parse_height(char)
    assert start_position is not None
    assert end_position is not None
    return heightmap, start_position, end_position


def list_adjacent(row, column):
    deltas = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    adjacent = []
    for delta_row, delta_column in deltas:
        adjacent.append((row + delta_row, column + delta_column))
    return adjacent


def part1(text: str):
    heightmap, start_position, end_position = parse(text)
    visited = np.zeros_like(heightmap, dtype=int)
    distances = np.zeros_like(heightmap, dtype=int)
    queue = q.Queue()
    queue.put(start_position)
    while not queue.empty():
        position = queue.get()
        if visited[position]:
            continue
        visited[position] = 1
        for adjacent_position in list_adjacent(*position):
            if not (0 <= adjacent_position[0] < heightmap.shape[0]):
                continue
            if not (0 <= adjacent_position[1] < heightmap.shape[1]):
                continue
            if visited[adjacent_position]:
                continue
            if heightmap[adjacent_position] > heightmap[position] + 1:
                continue
            distances[adjacent_position] = distances[position] + 1
            queue.put(adjacent_position)
    return distances[end_position]


def part2(text: str):
    heightmap, start_position, end_position = parse(text)
    visited = np.zeros_like(heightmap, dtype=int)
    distances = np.zeros_like(heightmap, dtype=int)
    queue = q.Queue()
    queue.put(end_position)
    while not queue.empty():
        position = queue.get()
        if visited[position]:
            continue
        visited[position] = 1
        for adjacent_position in list_adjacent(*position):
            if not (0 <= adjacent_position[0] < heightmap.shape[0]):
                continue
            if not (0 <= adjacent_position[1] < heightmap.shape[1]):
                continue
            if visited[adjacent_position]:
                continue
            if heightmap[position] > heightmap[adjacent_position] + 1:
                continue
            distances[adjacent_position] = distances[position] + 1
            queue.put(adjacent_position)
    result = 10000000
    for row in range(heightmap.shape[0]):
        for column in range(heightmap.shape[1]):
            if heightmap[row, column] == 0 and distances[row, column] != 0:
                result = min(result, distances[row, column])
    return result


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 31
    assert part1(real_text) == 497
    assert part2(test_text) == 29
    assert part2(real_text) == 492
