import argparse
import importlib
import sys
from pathlib import Path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            "This is a collection of solutions to Advent of Code 2022. There are 31 tasks for"
            " every day in December. Every task has two parts. Pick day and part and try the"
            " solution."
        )
    )
    parser.add_argument("day", type=int, help="number of the day for which the solution you need a solution")
    parser.add_argument("part", type=int, choices=[1, 2], help="part of the day")
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=None,
        help="provide input from a file, by default input is taken from stdin"
    )
    args = parser.parse_args()

    solutions = importlib.import_module(f"solutions.day_{args.day:02}")
    solve = solutions.part1 if args.part == 1 else solutions.part2
    input_text = Path(args.file).read_text() if args.file else sys.stdin.read()
    result = solve(input_text)
    print(result)
