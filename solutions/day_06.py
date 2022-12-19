import pathlib


day = int(__file__[-5:-3])
real_input_path = pathlib.Path(f"data/input-{day:02}-real.txt")


def part1(input: str):
    n = len(input)
    for i in range(n - 4):
        if len(set(input[i:i + 4])) == 4:
            return i + 4
    assert False


def test_part1():
    assert part1("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
    assert part1("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part1("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part1("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part1("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11
    assert part1(real_input_path.read_text()) == 1848


def part2(input: str):
    n = len(input)
    for i in range(n - 14):
        if len(set(input[i:i + 14])) == 14:
            return i + 14
    assert False


def test_part2():
    assert part2("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19
    assert part2("bvwbjplbgvbhsrlpgdmjqwftvncz") == 23
    assert part2("nppdvjthqldpwncqszvftbrmjlhg") == 23
    assert part2("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 29
    assert part2("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 26
    assert part2(real_input_path.read_text()) == 2308
