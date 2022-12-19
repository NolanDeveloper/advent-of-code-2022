import pathlib


day = int(__file__[-5:-3])
test_input_path = pathlib.Path(f"data/input-{day:02}-test.txt")
real_input_path = pathlib.Path(f"data/input-{day:02}-real.txt")


def parse(input: str):
    pass


def part1(input: str):
    pass


def test_part1():
    assert part1(test_input_path.read_text()) == 0
    assert part1(real_input_path.read_text()) == 0


def part2(input: str):
    pass


def test_part2():
    assert part2(test_input_path.read_text()) == 0
    assert part2(real_input_path.read_text()) == 0
