import pathlib


def parse(text: str):
    pass


def part1(text: str):
    pass


def part2(text: str):
    pass


def test():
    day = int(__file__[-5:-3])
    test_input_path = pathlib.Path(f"data/input-{day:02}-test.txt")
    real_input_path = pathlib.Path(f"data/input-{day:02}-real.txt")
    assert part1(test_input_path.read_text()) == 0
    assert part1(real_input_path.read_text()) == 0
    assert part2(test_input_path.read_text()) == 0
    assert part2(real_input_path.read_text()) == 0
