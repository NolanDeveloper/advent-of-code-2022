import pathlib
import enum


class Outcome(enum.Enum):
    Left = 0
    Even = 3
    Right = 6


class Shape(enum.Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


def play(a: Shape, b: Shape) -> Outcome:
    if a == b:
        return Outcome.Even
    left_wins = [
        (Shape.Rock, Shape.Scissors),
        (Shape.Paper, Shape.Rock),
        (Shape.Scissors, Shape.Paper),
    ]
    if (a, b) in left_wins:
        return Outcome.Left
    return Outcome.Right


def parse_play(input: str) -> Shape:
    options = {
        "A": Shape.Rock,
        "B": Shape.Paper,
        "C": Shape.Scissors,
        "X": Shape.Rock,
        "Y": Shape.Paper,
        "Z": Shape.Scissors,
    }
    return options[input]


def parse(input: str):
    lines = input.splitlines()
    tactics = []
    for line in lines:
        a, b = line.split()
        tactic = parse_play(a), parse_play(b)
        tactics.append(tactic)
    return tactics


def part1(input: str):
    tactics = parse(input)
    result = 0
    for a, b in tactics:
        outcome = play(a, b)
        result += outcome.value + b.value
    return result


def test_part1():
    input = pathlib.Path("data/input-02-test.txt").read_text()
    assert part1(input) == 15

    input = pathlib.Path("data/input-02-real.txt").read_text()
    assert part1(input) == 10310


def parse_outcome(input: str) -> Outcome:
    return {
        "X": Outcome.Left,
        "Y": Outcome.Even,
        "Z": Outcome.Right,
    }[input]


def parse2(input: str):
    lines = input.splitlines()
    tactics = []
    for line in lines:
        a, b = line.split()
        tactic = parse_play(a), parse_outcome(b)
        tactics.append(tactic)
    return tactics


def infer_our_shape(opponent: Shape, outcome: Outcome) -> Shape:
    if outcome == Outcome.Even:
        return opponent
    if outcome == Outcome.Left:
        return {
            Shape.Rock: Shape.Scissors,
            Shape.Paper: Shape.Rock,
            Shape.Scissors: Shape.Paper,
        }[opponent]
    assert outcome == Outcome.Right
    return {
        Shape.Rock: Shape.Paper,
        Shape.Paper: Shape.Scissors,
        Shape.Scissors: Shape.Rock,
    }[opponent]


def part2(input: str):
    tactics = parse2(input)
    result = 0
    for a, outcome in tactics:
        b = infer_our_shape(a, outcome)
        result += outcome.value + b.value
    return result


def test_part2():
    input = pathlib.Path("data/input-02-test.txt").read_text()
    assert part2(input) == 12

    input = pathlib.Path("data/input-02-real.txt").read_text()
    assert part2(input) == 14859
