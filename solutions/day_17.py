import pathlib
from collections import deque


# index is: (row, column)
# origin is bottom-left
ROCKS: list[set[(int, int)]] = [
    {(0, 0), (0, 1), (0, 2), (0, 3)},  # —
    {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},  # +
    {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)},  # ⅃
    {(0, 0), (1, 0), (2, 0), (3, 0)},  # |
    {(0, 0), (0, 1), (1, 0), (1, 1)},  # ⊞
]


def does_rock_hit_wall(rock: set[(int, int)], offset_row: int, offset_column: int, tunnel: set[(int, int)]) -> bool:
    for row, column in rock:
        r = row + offset_row
        c = column + offset_column
        if (r, c) in tunnel:
            return True
        if not (0 <= c < 7):
            return True
    return False


def bake_rock_into_tunnel(rock: set[(int, int)], offset_row: int, offset_column: int, tunnel: set[(int, int)]):
    top = 0
    for row, column in rock:
        r = row + offset_row
        c = column + offset_column
        top = max(top, r)
        tunnel.add((r, c))
    return top


def print_tunnel(tunnel: set[(int, int)]):
    top = max(row for row, _ in tunnel)
    bottom = min(row for row, _ in tunnel)
    for row in range(top - bottom + 1):
        for column in range(-1, 8):
            if column in [-1, 7]:
                print('#', end='')
            elif (top - row, column) in tunnel:
                print('#', end='')
            else:
                print(' ', end='')
        print('')


def part1(commands: str):
    commands = commands.strip()
    tunnel = {(0, column) for column in range(7)}
    rocks = deque(ROCKS)
    commands = deque(commands)
    top = 0
    for i in range(2022):
        rock = rocks.popleft()
        rocks.append(rock)
        falling_rock_position = [top + 4, 2]
        while True:
            # execute command
            command = commands.popleft()
            commands.append(command)
            if command == '<':
                delta_column = -1
            else:
                assert command == '>'
                delta_column = 1
            falling_rock_position[1] = falling_rock_position[1] + delta_column
            if does_rock_hit_wall(rock, *falling_rock_position, tunnel):
                falling_rock_position[1] = falling_rock_position[1] - delta_column
            # fall down
            falling_rock_position[0] -= 1
            if does_rock_hit_wall(rock, *falling_rock_position, tunnel):
                falling_rock_position[0] += 1
                top = max(top, bake_rock_into_tunnel(rock, *falling_rock_position, tunnel))
                break
    return max(row for row, _ in tunnel)


def part2(commands: str):
    commands = commands.strip()
    tunnel = {(0, column) for column in range(7)}
    rock_index = 0
    command_index = 0
    number_of_rows_skipped = 0
    fast_falls = {}
    rocks_fallen = 0
    total_number_of_rocks = 1000000000000
    top = 0
    while rocks_fallen < total_number_of_rocks:
        rock = ROCKS[rock_index]
        falling_rock_position = [top + 4, 2]
        falling_time = 0
        start_command_index = command_index
        while True:
            falling_time += 1
            # execute command
            command = commands[command_index]
            command_index = (command_index + 1) % len(commands)
            if command == '<':
                delta_column = -1
            else:
                assert command == '>'
                delta_column = 1
            falling_rock_position[1] = falling_rock_position[1] + delta_column
            if does_rock_hit_wall(rock, *falling_rock_position, tunnel):
                falling_rock_position[1] = falling_rock_position[1] - delta_column
            # fall down
            falling_rock_position[0] -= 1
            if does_rock_hit_wall(rock, *falling_rock_position, tunnel):
                falling_rock_position[0] += 1
                if falling_time == 4 and rock_index == 0 and number_of_rows_skipped == 0:
                    top_mask = sum(1 << column for row, column in tunnel if row == top)
                    key = (start_command_index, top_mask)
                    if key in fast_falls:
                        previous_rocks_fallen, previous_top = fast_falls[key]
                        loop_length = rocks_fallen - previous_rocks_fallen
                        number_of_loops = (total_number_of_rocks - rocks_fallen) // loop_length
                        number_of_rows_skipped = (top - previous_top) * number_of_loops
                        rocks_fallen += number_of_loops * loop_length - 1
                    else:
                        fast_falls[key] = (rocks_fallen, top)
                top = max(top, bake_rock_into_tunnel(rock, *falling_rock_position, tunnel))
                break
        rock_index = (rock_index + 1) % len(ROCKS)
        rocks_fallen += 1
    return number_of_rows_skipped + max(row for row, _ in tunnel) - 1


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 3068
    assert part1(real_text) == 3175
    assert part2(test_text) == 1514285714288
    assert part2(real_text) == 1555113636385
