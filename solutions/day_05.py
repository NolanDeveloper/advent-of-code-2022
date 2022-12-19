import pathlib
from dataclasses import dataclass


day = int(__file__[-5:-3])


@dataclass
class Move:
    amount: int
    source: int
    destination: int


def parse(input: str) -> tuple[list[list[str]], list[Move]]:
    lines = input.splitlines()
    current_line = 0
    # parse crates
    crates = []
    while current_line < len(lines):
        line = lines[current_line]
        current_line += 1
        if line[1] == '1':
            break
        section = []
        for i in range(1, len(line), 4):
            section.append(line[i])
        crates.append(section)
    current_line += 1
    # rearrange creates column-wise instead of row-wise
    number_of_stacks = len(crates[0])
    stacks = []
    for i in range(number_of_stacks):
        stack = []
        for row in crates[::-1]:
            if row[i] != ' ':
                stack.append(row[i])
        stacks.append(stack)
    # parse moves
    moves = []
    while current_line < len(lines):
        line = lines[current_line]
        current_line += 1
        parts = line.split(" ")
        move = Move(
            amount=int(parts[1]),
            source=int(parts[3]) - 1,
            destination=int(parts[5]) - 1
        )
        moves.append(move)
    return stacks, moves


def part1(input: str):
    stacks, moves = parse(input)
    for move in moves:
        for _ in range(move.amount):
            crate = stacks[move.source].pop()
            stacks[move.destination].append(crate)
    tops = ""
    for stack in stacks:
        tops += stack[-1]
    return tops


def test_part1():
    input = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    assert part1(input) == "CMZ"

    input = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(input) == "TBVFVDZPN"


def part2(input: str):
    stacks, moves = parse(input)
    for move in moves:
        src = stacks[move.source]
        dst = stacks[move.destination]
        dst.extend(src[-move.amount:])
        del src[-move.amount:]
    tops = ""
    for stack in stacks:
        tops += stack[-1]
    return tops


def test_part2():
    input = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    assert part2(input) == "MCD"

    input = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part2(input) == "VLCWHTDSZ"
