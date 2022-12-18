import argparse
import importlib
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            "This is a collection of solutions to Advent of Code 2022. There are 31 tasks for"
            " every day in December. Every task has two parts. Pick day and part and try the"
            " solution."
        )
    )
    parser.add_argument("day", type=int)
    parser.add_argument("part", type=int, choices=[1, 2])
    args = parser.parse_args()

    solutions = importlib.import_module(f"solutions.day_{args.day:02}")
    solve = solutions.part1 if args.part == 1 else solutions.part2
    result = solve(sys.stdin.read())
    print(result)
