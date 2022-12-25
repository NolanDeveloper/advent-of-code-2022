import pathlib
from collections import defaultdict


def parse(text: str):
    rates = {}
    adjacency = {}
    for line in text.splitlines():
        parts = line.split()
        valve = parts[1]
        rate = int(parts[4][5:-1])
        adjacent = list(map(lambda s: s.removesuffix(","), parts[9:]))
        adjacency[valve] = adjacent
        rates[valve] = rate
    return adjacency, rates


def part1(text: str):
    adjacency, rates = parse(text)
    effective_valves = set(valve for valve in rates.keys() if rates[valve] != 0)
    # calculate distance between valves using Floyd-Warshall
    distances = defaultdict(lambda: defaultdict(lambda: 100))
    for valve, adjacent in adjacency.items():
        distances[valve][valve] = 0
        for adjacent_valve in adjacent:
            distances[valve][adjacent_valve] = 1
    for i in range(len(rates.keys())):
        v = list(adjacency.keys())[i]
        for a in list(adjacency.keys()):
            for b in list(adjacency.keys()):
                distances[a][b] = min(distances[a][b], distances[a][v] + distances[v][b])
    opened_valves = set()

    def max_pressure_released_starting_from(valve: str, minutes_left: int):
        nonlocal opened_valves
        if opened_valves == effective_valves or minutes_left <= 2:
            return 0
        minutes_left -= 1
        pressure_released_here = rates[valve] * minutes_left
        result = pressure_released_here
        opened_valves |= {valve}
        for another_valve in effective_valves - opened_valves:
            pressure_released_there = max_pressure_released_starting_from(
                another_valve,
                minutes_left - distances[valve][another_valve]
            )
            result = max(result, pressure_released_here + pressure_released_there)
        opened_valves -= {valve}
        return result

    return max(
        max_pressure_released_starting_from(valve, minutes_left=30 - distances['AA'][valve])
        for valve in effective_valves
    )


def part2(text: str):
    adjacency, rates = parse(text)
    effective_valves = set(valve for valve in rates.keys() if rates[valve] != 0)
    # calculate distance between valves using Floyd-Warshall
    distances = defaultdict(lambda: defaultdict(lambda: 100))
    for valve, adjacent in adjacency.items():
        distances[valve][valve] = 0
        for adjacent_valve in adjacent:
            distances[valve][adjacent_valve] = 1
    for i in range(len(rates.keys())):
        v = list(adjacency.keys())[i]
        for a in list(adjacency.keys()):
            for b in list(adjacency.keys()):
                distances[a][b] = min(distances[a][b], distances[a][v] + distances[v][b])
    opened_valves = set()

    def max_pressure_released_starting_from(
            my_position: str,
            my_time: int,
            elephant_position: str,
            elephant_time: int
    ):
        nonlocal number_of_my_valves
        nonlocal opened_valves
        if my_time <= 2 and len(opened_valves) < number_of_my_valves or\
                elephant_time <= 2 and len(opened_valves) >= number_of_my_valves:
            return 0
        result = 0
        valves = list(effective_valves - opened_valves)
        for another_valve in valves:
            opened_valves |= {another_valve}
            if len(opened_valves) < number_of_my_valves:
                # try to open myself
                release_duration = my_time - distances[my_position][another_valve] - 1
                if release_duration > 0:
                    pressure_released = rates[another_valve] * release_duration
                    result = max(result, pressure_released + max_pressure_released_starting_from(
                        another_valve,
                        release_duration,
                        elephant_position,
                        elephant_time
                    ))
            else:
                # ask elephant to open
                release_duration = elephant_time - distances[elephant_position][another_valve] - 1
                if release_duration > 0:
                    pressure_released = rates[another_valve] * release_duration
                    result = max(result, pressure_released + max_pressure_released_starting_from(
                        my_position,
                        my_time,
                        another_valve,
                        release_duration
                    ))
            opened_valves -= {another_valve}
        return result

    answer = 0
    for number_of_my_valves in range(len(effective_valves)):
        answer = max(answer, max_pressure_released_starting_from('AA', 26, 'AA', 26))
    return answer


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 1651
    assert part1(real_text) == 1728
    assert part2(test_text) == 1707
    assert part2(real_text) == 2304
