import pathlib


def parse(text: str):
    return [int(line.strip()) for line in text.splitlines()]


def solve(numbers: list[int], number_of_mixes: int) -> int:
    n = len(numbers)
    nxt = [(i + 1) % n for i in range(n)]
    prv = [(i - 1) % n for i in range(n)]

    for a in range(number_of_mixes * n):
        a %= n
        t = numbers[a] % (n - 1)
        if t == 0:
            continue
        # 1. detach a
        nxt[prv[a]] = nxt[a]
        prv[nxt[a]] = prv[a]
        b = a
        for _ in range(t):
            b = nxt[b]
        # 2. insert a after b
        prv[a] = b
        nxt[a] = nxt[b]
        prv[nxt[b]] = a
        nxt[b] = a

    numbers_reordered = [numbers[0]]
    i = nxt[0]
    while i != 0:
        numbers_reordered.append(numbers[i])
        i = nxt[i]
    assert len(numbers_reordered) == n
    zero_at = numbers_reordered.index(0)
    interesting_numbers = [
        numbers_reordered[(zero_at + 1000) % n],
        numbers_reordered[(zero_at + 2000) % n],
        numbers_reordered[(zero_at + 3000) % n],
    ]
    return sum(interesting_numbers)


def part1(text: str):
    numbers = parse(text)
    return solve(numbers, 1)


def part2(text: str):
    numbers = parse(text)
    numbers = [811589153 * x for x in numbers]
    return solve(numbers, 10)


def test():
    print()
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == (4 + (-3) + 2)
    assert part1(real_text) == 7278
    assert part2(test_text) == 1623178306
    assert part2(real_text) == 14375678667089
