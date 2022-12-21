import pathlib


def part1(text: str):
    current_cycle = 0
    register_x = 1
    result = 0

    def cycle():
        nonlocal current_cycle
        nonlocal register_x
        nonlocal result
        current_cycle += 1
        if (current_cycle - 20) % 40 == 0:
            signal_strength = current_cycle * register_x
            result += signal_strength

    for line in text.splitlines():
        parts = line.split()
        if parts[0] == 'noop':
            cycle()
        elif parts[0] == 'addx':
            cycle()
            cycle()
            value = int(parts[1])
            register_x += value
    return result


def part2(text: str):
    current_cycle = 0
    register_x = 1
    display = [[' ' for _ in range(40)] for _ in range(6)]

    def cycle():
        nonlocal current_cycle
        nonlocal register_x
        current_cycle += 1
        current_row = ((current_cycle - 1) // 40) % 6
        current_column = (current_cycle - 1) % 40
        if register_x - 1 <= current_column <= register_x + 1:
            display[current_row][current_column] = '#'

    for line in text.splitlines():
        parts = line.split()
        if parts[0] == 'noop':
            cycle()
        elif parts[0] == 'addx':
            cycle()
            cycle()
            value = int(parts[1])
            register_x += value
    return '\n'.join(''.join(row) for row in display)


def test():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 13140
    assert part1(real_text) == 13820

    expected_result = """
#### #  #  ##  ###  #  #  ##  ###  #  # 
   # # #  #  # #  # # #  #  # #  # # #  
  #  ##   #    #  # ##   #    #  # ##   
 #   # #  # ## ###  # #  # ## ###  # #  
#    # #  #  # # #  # #  #  # # #  # #  
#### #  #  ### #  # #  #  ### #  # #  # """[1:]
    assert part2(real_text) == expected_result
