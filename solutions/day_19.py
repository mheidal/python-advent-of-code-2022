import functools
import re
from typing import NamedTuple, Tuple, List, Set


class Cost(NamedTuple):
    ore: int
    clay: int
    obs: int


class Blueprint(NamedTuple):
    id: int
    ore: Cost
    clay: Cost
    obs: Cost
    geode: Cost
    max_ore: int
    max_clay: int
    max_obs: int


class Robots(NamedTuple):
    ore: int
    clay: int
    obs: int
    geode: int


class Inventory(NamedTuple):
    ore: int
    clay: int
    obs: int
    geode: int


def create_blueprint(line) -> Blueprint:
    blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = list(
        map(int, re.findall("\\d+", line))
    )
    return Blueprint(
        blueprint_id,
        Cost(ore_ore, 0, 0),
        Cost(clay_ore, 0, 0),
        Cost(obs_ore, obs_clay, 0),
        Cost(geo_ore, 0, geo_obs),
        max(geo_ore, clay_ore, obs_ore),
        obs_clay,
        geo_obs,
    )


def get_blueprints() -> List[Blueprint]:
    blueprints: List[Blueprint] = []
    with open(f"../inputs/day_19.txt", "r") as input_file:
        for line in input_file.read().splitlines():
            blueprints.append(create_blueprint(line))
    return blueprints


@functools.cache
def get_next_states(
    blueprint: Blueprint, robots: Robots, inventory: Inventory
) -> List[Tuple[Robots, Inventory]]:
    next_states: List[Tuple[Robots, Inventory]] = []
    produced = Inventory(
        inventory.ore + robots.ore,
        inventory.clay + robots.clay,
        inventory.obs + robots.obs,
        inventory.geode + robots.geode,
    )

    if inventory.ore >= blueprint.geode.ore and inventory.obs >= blueprint.geode.obs:
        next_states.append(
            (
                Robots(robots.ore, robots.clay, robots.obs, robots.geode + 1),
                Inventory(
                    produced.ore - blueprint.geode.ore,
                    produced.clay,
                    produced.obs - blueprint.geode.obs,
                    produced.geode,
                ),
            )
        )
    else:
        if inventory.ore >= blueprint.ore.ore and robots.ore < blueprint.max_ore:
            next_states.append(
                (
                    Robots(robots.ore + 1, robots.clay, robots.obs, robots.geode),
                    Inventory(
                        produced.ore - blueprint.ore.ore,
                        produced.clay,
                        produced.obs,
                        produced.geode,
                    ),
                )
            )
        if inventory.ore >= blueprint.clay.ore and robots.clay < blueprint.max_clay:
            next_states.append(
                (
                    Robots(robots.ore, robots.clay + 1, robots.obs, robots.geode),
                    Inventory(
                        produced.ore - blueprint.clay.ore,
                        produced.clay,
                        produced.obs,
                        produced.geode,
                    ),
                )
            )
        if (
            inventory.ore >= blueprint.obs.ore
            and inventory.clay >= blueprint.obs.clay
            and robots.obs < blueprint.max_obs
        ):
            next_states.append(
                (
                    Robots(robots.ore, robots.clay, robots.obs + 1, robots.geode),
                    Inventory(
                        produced.ore - blueprint.obs.ore,
                        produced.clay - blueprint.obs.clay,
                        produced.obs,
                        produced.geode,
                    ),
                )
            )
        next_states.append((robots, produced))
    limit = 2
    next_states = [
        (
            r,
            Inventory(
                min(i.ore, blueprint.max_ore * limit),
                min(i.clay, blueprint.max_clay * limit),
                min(i.obs, blueprint.max_obs * limit),
                i.geode,
            ),
        )
        for r, i in next_states
    ]
    return next_states


def investigate_blueprint(blueprint: Blueprint, start_time: int) -> int:
    get_next_states.cache_clear()
    prev_states: Set[Tuple[Blueprint, Robots, Inventory, int]] = set()
    max_geodes = 0
    queue: Set[Tuple[Robots, Inventory, int]] = {
        (Robots(1, 0, 0, 0), Inventory(0, 0, 0, 0), start_time)
    }
    while queue:
        robots, inventory, time_remaining = queue.pop()
        if time_remaining == 0:
            max_geodes = max(max_geodes, inventory.geode)
        else:
            cur_state = (blueprint, robots, inventory, time_remaining)
            if cur_state not in prev_states:
                prev_states.add(cur_state)
                for next_robots, next_inventory in get_next_states(
                    blueprint, robots, inventory
                ):
                    if (next_robots, next_inventory, time_remaining - 1) not in queue:
                        queue.add((next_robots, next_inventory, time_remaining - 1))
    return max_geodes


def part_1():
    blueprints = get_blueprints()
    geode_counts = [investigate_blueprint(blueprint, 24) for blueprint in blueprints]
    qualities = 0
    for i, geode_count in enumerate(geode_counts):
        qualities += (i + 1) * geode_count
    print(f"Part 1: {qualities}")


def part_2():
    blueprints = get_blueprints()[:3]
    results = {investigate_blueprint(blueprint, 32) for blueprint in blueprints}
    prod = 1
    for geode_count in results:
        prod *= geode_count
    print(f"Part 2: {prod}")


if __name__ == "__main__":
    part_1()
    part_2()
