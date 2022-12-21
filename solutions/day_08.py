import pathlib
import numpy
import math

day = int(__file__[-5:-3])
test_input_path = pathlib.Path(f"data/input-{day:02}-test.txt")
real_input_path = pathlib.Path(f"data/input-{day:02}-real.txt")


def parse(text: str) -> numpy.ndarray:
    data = []
    lines = text.splitlines()
    number_of_rows = len(lines)
    number_of_columns = len(lines[0].strip())
    for line in lines:
        line = line.strip()
        data.extend(int(c) for c in line)
    result = numpy.array(data)
    result = result.reshape((number_of_rows, number_of_columns))
    return result


def part1(text: str):
    heights = parse(text)
    to_bottom = numpy.pad(
        numpy.maximum.accumulate(heights),
        pad_width=((1, 0), (0, 0)),
        constant_values=-1
    )[:-1, :]
    to_top = numpy.pad(
        numpy.maximum.accumulate(heights[::-1, :])[::-1, :],
        pad_width=((0, 1), (0, 0)),
        constant_values=-1
    )[1:, :]
    to_right = numpy.pad(
        numpy.maximum.accumulate(heights, axis=1),
        pad_width=((0, 0), (1, 0)),
        constant_values=-1
    )[:, :-1]
    to_left = numpy.pad(
        numpy.maximum.accumulate(heights[:, ::-1], axis=1)[:, ::-1],
        pad_width=((0, 0), (0, 1)),
        constant_values=-1
    )[:, 1:]
    least_visible_height = numpy.minimum(to_bottom, numpy.minimum(to_top, numpy.minimum(to_right, to_left)))
    return numpy.count_nonzero(heights > least_visible_height)


def test_part1():
    assert part1(test_input_path.read_text()) == 21
    assert part1(real_input_path.read_text()) == 1733


def part2(text: str):
    heights = parse(text)
    print()
    print(heights)
    number_of_rows, number_of_columns = heights.shape
    result = 0
    for row in range(number_of_rows):
        for column in range(number_of_columns):
            height = heights[row, column]

            def count_trees(delta_row, delta_column):
                current_row = row + delta_row
                current_column = column + delta_column
                number_of_visible_trees = 0
                while 0 <= current_row < number_of_rows and 0 <= current_column < number_of_columns:
                    number_of_visible_trees += 1
                    if heights[current_row, current_column] >= height:
                        break
                    current_row += delta_row
                    current_column += delta_column
                return number_of_visible_trees

            visible_trees = [
                count_trees(-1, 0),
                count_trees(1, 0),
                count_trees(0, -1),
                count_trees(0, 1)
            ]
            scientific_score = math.prod(visible_trees)
            result = max(result, scientific_score)
    return result


def test_part2():
    assert part2(test_input_path.read_text()) == 8
    assert part2(real_input_path.read_text()) == 284648
