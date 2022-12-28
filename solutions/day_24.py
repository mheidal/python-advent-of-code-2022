from enum import Enum
from typing import Dict, Tuple, NamedTuple, List


class Coord(NamedTuple):
    x: int
    y: int


class Facing(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"


class Blizzard(NamedTuple):
    pos: Coord
    facing: Facing


def get_next_position_for_blizzard(blizzard: Blizzard, max_x, max_y):
    x: int
    y: int
    if blizzard.facing == Facing.UP:
        x = blizzard.pos.x + 0
        y = blizzard.pos.y - 1
    elif blizzard.facing == Facing.RIGHT:
        x = blizzard.pos.x + 1
        y = blizzard.pos.y + 0
    elif blizzard.facing == Facing.DOWN:
        x = blizzard.pos.x + 0
        y = blizzard.pos.y + 1
    else:
        x = blizzard.pos.x - 1
        y = blizzard.pos.y + 0
    return Blizzard(Coord(x % max_x, y % max_y), blizzard.facing)


def get_setup() -> Tuple[List[Blizzard], Coord, Coord, int, int]:
    """
    List of blizzard positions to start with, start position, end position, maximum x, maximum y position achievable
    """
    with open(f"../inputs/day_24.txt", "r") as input_file:
        lines = input_file.read().split("\n")
        max_x = len(lines[0]) - 2
        max_y = len(lines) - 2
        blizzards = []
        for row_index, row in enumerate(lines):
            for col_index, entry in enumerate(row):
                if entry == "#":
                    continue
                pos = Coord(col_index - 1, row_index - 1)
                if row_index == 0:
                    if entry == ".":
                        start = pos
                elif row_index == len(lines) - 1:
                    if entry == ".":
                        end = pos
                else:
                    if entry == "^":
                        blizzards.append(Blizzard(pos, Facing.UP))
                    elif entry == ">":
                        blizzards.append(Blizzard(pos, Facing.RIGHT))
                    elif entry == "v":
                        blizzards.append(Blizzard(pos, Facing.DOWN))
                    elif entry == "<":
                        blizzards.append(Blizzard(pos, Facing.LEFT))
    assert start is not None
    assert end is not None
    return blizzards, start, end, max_x, max_y


def do_bfs(
    start_packet: Tuple[Coord, int],
    target_pos: Coord,
    blizzard_steps: Dict[int, List[Blizzard]],
    max_x: int,
    max_y: int,
) -> int:
    queue: List[Tuple[Coord, int]] = [start_packet]
    while queue:
        current_position, timestamp = queue.pop(0)
        if current_position == target_pos:
            return timestamp
        if timestamp + 1 not in blizzard_steps:
            next_blizzards = []
            for blizzard in blizzard_steps[timestamp]:
                next_blizzard = get_next_position_for_blizzard(
                    blizzard, max_x=max_x, max_y=max_y
                )
                next_blizzards.append(next_blizzard)
            print(f"Generated {timestamp + 1}. Queue length is {len(queue)}")
            blizzard_steps[timestamp + 1] = next_blizzards
        else:
            next_blizzards = blizzard_steps[timestamp + 1]
        next_positions: List[Coord] = [
            Coord(current_position.x + 0, current_position.y + 0),  # wait
            Coord(current_position.x + 1, current_position.y + 0),  # right
            Coord(current_position.x + 0, current_position.y + 1),  # down
            Coord(current_position.x - 1, current_position.y + 0),  # left
            Coord(current_position.x + 0, current_position.y - 1),  # up
        ]
        for next_position in next_positions:
            if (
                (
                    next_position == target_pos
                    or next_position == start_packet[0]
                    or (0 <= next_position.x < max_x and 0 <= next_position.y < max_y)
                )
                and not any(
                    [blizzard.pos == next_position for blizzard in next_blizzards]
                )
                and (next_position, timestamp + 1) not in queue
            ):
                queue.append((next_position, timestamp + 1))


def part_1():
    start_blizzard, start, end, max_x, max_y = get_setup()
    blizzard_steps: Dict[int, List[Blizzard]] = {0: start_blizzard}
    print(do_bfs((start, 0), end, blizzard_steps, max_x, max_y))


def part_2():
    start_blizzard, start, end, max_x, max_y = get_setup()
    blizzard_steps: Dict[int, List[Blizzard]] = {0: start_blizzard}
    time_to_end = do_bfs((start, 0), end, blizzard_steps, max_x, max_y)
    time_back_to_start = do_bfs((end, time_to_end), start, blizzard_steps, max_x, max_y)
    print(do_bfs((start, time_back_to_start), end, blizzard_steps, max_x, max_y))


if __name__ == "__main__":
    part_1()
    part_2()
