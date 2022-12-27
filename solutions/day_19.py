import functools
import operator
import pathlib
from collections import namedtuple
from typing import Callable

Resources = namedtuple('Resources', ('ore', 'clay', 'obsidian', 'geode'), defaults=(0, 0, 0, 0))


def zip_with(f: Callable[[Resources, Resources], Resources], a: Resources, b: Resources) -> Resources:
    assert len(a) == len(b)
    return Resources(*(f(a[i], b[i]) for i in range(len(a))))


def add_resources(a: Resources, b: Resources) -> Resources:
    return Resources(
        ore=a.ore + b.ore,
        clay=a.clay + b.clay,
        obsidian=a.obsidian + b.obsidian,
        geode=a.geode + b.geode
    )


def sub_resources(a: Resources, b: Resources) -> Resources:
    return Resources(
        ore=a.ore - b.ore,
        clay=a.clay - b.clay,
        obsidian=a.obsidian - b.obsidian,
        geode=a.geode - b.geode
    )


def is_enough(resources: Resources, blueprint: Resources) -> bool:
    return resources.ore >= blueprint.ore and resources.clay >= blueprint.clay and \
           resources.obsidian >= blueprint.obsidian and resources.geode >= blueprint.geode


def parse(text: str):
    blueprints = []
    for line in text.splitlines():
        parts = line.split()
        ore = Resources(ore=int(parts[6]))
        clay = Resources(ore=int(parts[12]))
        obsidian = Resources(ore=int(parts[18]), clay=int(parts[21]))
        geode = Resources(ore=int(parts[27]), obsidian=int(parts[30]))
        blueprints.append((ore, clay, obsidian, geode))
    return blueprints


def max_geodes(blueprints: Resources, time_limit: int = 24) -> int:
    ore_blueprint, clay_blueprint, obsidian_blueprint, geode_blueprint = blueprints
    cache = {}
    # There's no reason to mine more than we can spend in one minute
    max_ore_requirement = max(ore_blueprint.ore - 1, clay_blueprint.ore, obsidian_blueprint.ore, geode_blueprint.ore)
    max_clay_requirement = obsidian_blueprint.clay
    max_obsidian_requirement = geode_blueprint.obsidian

    t = time_limit + 1

    def max_geodes_starting_from(current_minute: int, robots: Resources, resources: Resources, current_max: int) -> int:
        time_left = time_limit - current_minute
        max_ore_to_spend = time_left * max_ore_requirement
        max_clay_to_spend = time_left * max_clay_requirement
        max_obsidian_to_spend = time_left * max_obsidian_requirement
        resources = resources._replace(
            ore=min(resources.ore, max_ore_to_spend),
            clay=min(resources.clay, max_clay_to_spend),
            obsidian=min(resources.obsidian, max_obsidian_to_spend),
        )
        key = (current_minute, robots, resources)
        if key in cache:
            return cache[key]
        potential_geodes_gather = resources.geode + robots.geode * time_left + (time_left - 1) * time_left // 2
        if potential_geodes_gather < current_max:
            return 0
        if current_minute >= time_limit:
            cache[key] = resources.geode
            return cache[key]
        resources_with_mined = add_resources(resources, robots)
        geodes = resources_with_mined.geode
        resources_with_mined = resources_with_mined._replace(geode=0)
        result = max_geodes_starting_from(current_minute + 1, robots, resources_with_mined, current_max - geodes)
        if robots.ore < max_ore_requirement and is_enough(resources, ore_blueprint):
            new_robots = add_resources(robots, Resources(ore=1))
            new_resources = sub_resources(resources_with_mined, ore_blueprint)
            result = max(result, max_geodes_starting_from(current_minute + 1, new_robots, new_resources, result))
        if robots.clay < max_clay_requirement and is_enough(resources, clay_blueprint):
            new_robots = add_resources(robots, Resources(clay=1))
            new_resources = sub_resources(resources_with_mined, clay_blueprint)
            result = max(result, max_geodes_starting_from(current_minute + 1, new_robots, new_resources, result))
        if robots.obsidian < max_obsidian_requirement and is_enough(resources, obsidian_blueprint):
            new_robots = add_resources(robots, Resources(obsidian=1))
            new_resources = sub_resources(resources_with_mined, obsidian_blueprint)
            result = max(result, max_geodes_starting_from(current_minute + 1, new_robots, new_resources, result))
        if is_enough(resources, geode_blueprint):
            new_robots = add_resources(robots, Resources(geode=1))
            new_resources = sub_resources(resources_with_mined, geode_blueprint)
            result = max(result, max_geodes_starting_from(current_minute + 1, new_robots, new_resources, result))
        result += geodes
        cache[key] = result
        nonlocal t
        if current_minute < t:
            t = current_minute
            print(f'{t} ')
        return result

    return max_geodes_starting_from(0, Resources(ore=1), Resources(), 0)


def part1(text: str):
    blueprints = parse(text)
    result = 0
    for i, blueprint in enumerate(blueprints, start=1):
        number_of_geodes = max_geodes(blueprint)
        quality_level = number_of_geodes * i
        result += quality_level
    return result


def part2(text: str):
    blueprints = parse(text)
    result = 1
    for blueprint in blueprints[:3]:
        number_of_geodes = max_geodes(blueprint, time_limit=32)
        print(number_of_geodes)
        result *= number_of_geodes
    return result


def test_part1():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part1(test_text) == 33
    assert part1(real_text) == 817


def test_part2():
    day = int(__file__[-5:-3])
    test_text = pathlib.Path(f"data/input-{day:02}-test.txt").read_text()
    real_text = pathlib.Path(f"data/input-{day:02}-real.txt").read_text()
    assert part2(test_text) == 56 * 62
    assert part2(real_text) == 4216
