import functools
import pathlib


def parse(text: str):
    pairs = text.split('\n\n')
    result = []
    for pair in pairs:
        a, b = pair.split()
        a = eval(a)
        b = eval(b)
        result.append((a, b))
    return result


def is_less(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a < b
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]
    i = 0
    while i < len(a) and i < len(b) and a[i] == b[i]:
        i += 1
    if i < len(a) and i < len(b):
        if is_less(a[i], b[i]):
            return True
        if is_less(b[i], a[i]):
            return False
        i += 1
    return len(a) < len(b)


def part1(text: str):
    pairs = parse(text)
    result = 0
    for i, (a, b) in enumerate(pairs, 1):
        if is_less(a, b):
            result += i
    return result


def compare(a, b):
    if is_less(a, b):
        return -1
    return 1


def part2(text: str):
    pairs = parse(text)
    packets = [[[2]], [[6]]]
    for pair in pairs:
        packets.extend(pair)
    packets.sort(reverse=False, key=functools.cmp_to_key(compare))
    a = 1 + packets.index([[2]])
    b = 1 + packets.index([[6]])
    return a * b


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 13
    assert part1(real_text) == 5555
    assert part2(test_text) == 140
    assert part2(real_text) == 22852
