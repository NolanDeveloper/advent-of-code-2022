import pathlib


def parse(text: str):
    pass


def part1(text: str):
    pass


def part2(text: str):
    pass


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 0
    assert part1(real_text) == 0
    assert part2(test_text) == 0
    assert part2(real_text) == 0
