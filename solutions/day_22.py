from enum import IntEnum
from typing import List, Tuple, Dict, NamedTuple
import re

Grid = List[List[str]]
CoordId = Tuple[int, int]


class Facing(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    NOTSET = -1


class Result(NamedTuple):
    pos: CoordId
    facing: Facing


class Coord:
    def __init__(self, right: Result, down: Result, left: Result, up: Result):
        self.right = right
        self.down = down
        self.left = left
        self.up = up

    def go(self, facing: Facing) -> Result:
        if facing == Facing.RIGHT:
            return self.right
        elif facing == Facing.DOWN:
            return self.down
        elif facing == Facing.LEFT:
            return self.left
        elif facing == Facing.UP:
            return self.up
        raise ValueError


def get_turn_direction(direction: str, facing: Facing) -> Facing:
    if direction == "L":
        if facing == Facing.RIGHT:
            return Facing.UP
        elif facing == Facing.DOWN:
            return Facing.RIGHT
        elif facing == Facing.LEFT:
            return Facing.DOWN
        elif facing == Facing.UP:
            return Facing.LEFT
    elif direction == "R":
        if facing == Facing.RIGHT:
            return Facing.DOWN
        elif facing == Facing.DOWN:
            return Facing.LEFT
        elif facing == Facing.LEFT:
            return Facing.UP
        elif facing == Facing.UP:
            return Facing.RIGHT


def get_index_of_leftmost_coord(grid: Grid, row_index: int) -> int:
    row = grid[row_index]
    for i, coord in enumerate(row):
        if coord != " ":
            return i
    raise ValueError


def get_index_of_rightmost_coord(grid: Grid, row_index: int) -> int:
    row = grid[row_index]
    for i, coord in reversed(list(enumerate(row))):
        if coord != " ":
            return i
    raise ValueError


def get_index_of_lowest_coord(grid: Grid, col_index: int) -> int:
    col = [row[col_index] for row in grid]
    for i, coord in reversed(list(enumerate(col))):
        if coord != " ":
            return i
    raise ValueError


def get_index_of_highest_coord(grid: Grid, col_index: int) -> int:
    col = [row[col_index] for row in grid]
    for i, coord in enumerate(col):
        if coord != " ":
            return i
    raise ValueError


def is_valid_position(grid, row_index, col_index):
    return -1 < row_index < len(grid) and -1 < col_index < len(grid[0])


def part_1():
    with open(f"../inputs/day_22.txt", "r") as input_file:
        grid_section, directions_section = input_file.read().split("\n\n")
    grid = [list(line) for line in grid_section.split("\n")]
    coords: Dict[CoordId, Coord] = {}
    for row_index, row in enumerate(grid):
        for col_index, entry in enumerate(row):
            if entry != " ":
                positions: List[Result] = [Result((-1, -1), Facing.NOTSET)] * 4  # r, d, l, u

                # Right
                if (
                    is_valid_position(grid, row_index, col_index + 1)
                    and grid[row_index][col_index + 1] != " "
                ):
                    positions[0] = Result((row_index, col_index + 1), Facing.RIGHT)
                else:
                    positions[0] = Result((row_index, get_index_of_leftmost_coord(grid, row_index)), Facing.RIGHT)

                # Down
                if (
                    is_valid_position(grid, row_index + 1, col_index)
                    and grid[row_index + 1][col_index] != " "
                ):
                    positions[1] = Result((row_index + 1, col_index), Facing.DOWN)
                else:
                    positions[1] = Result((get_index_of_highest_coord(grid, col_index), col_index), Facing.DOWN)

                # Left
                if (
                    is_valid_position(grid, row_index, col_index - 1)
                    and grid[row_index][col_index - 1] != " "
                ):
                    positions[2] = Result((row_index, col_index - 1), Facing.LEFT)
                else:
                    positions[2] = Result((row_index, get_index_of_rightmost_coord(grid, row_index)), Facing.LEFT)

                # Up
                if (
                    is_valid_position(grid, row_index - 1, col_index)
                    and grid[row_index - 1][col_index] != " "
                ):

                    positions[3] = Result((row_index - 1, col_index), Facing.UP)
                else:
                    positions[3] = Result((get_index_of_lowest_coord(grid, col_index), col_index), Facing.UP)

                # Check each to ensure it doesn't lead into a blocker
                for action, result in enumerate(positions):
                    i, j = result.pos
                    if grid[i][j] == "#":
                        positions[action] = Result((row_index, col_index), result.facing)

                coords[(row_index, col_index)] = Coord(*positions)

    directions = re.findall("\\D+|\\d+", directions_section)

    current = Result((0, get_index_of_leftmost_coord(grid, 0)), Facing.RIGHT)
    hist: Dict[CoordId, Facing] = {current.pos: current.facing}

    def disp():
        s = ""
        for row_index, row in enumerate(grid):
            for col_index, entry in enumerate(row):
                if (pos := (row_index, col_index)) in hist:
                    if hist[pos] == Facing.RIGHT:
                        s += ">"
                    elif hist[pos] == Facing.DOWN:
                        s += "v"
                    elif hist[pos] == Facing.LEFT:
                        s += "<"
                    elif hist[pos] == Facing.UP:
                        s += "^"
                else:
                    s += entry
            s += "\n"
        print(s)

    for action in directions:
        if action in "LR":
            current = Result(current.pos, get_turn_direction(action, current.facing))
            hist[current.pos] = current.facing
        else:
            for _ in range(int(action)):
                last = current.pos
                current = coords[current.pos].go(current.facing)
                hist[current.pos] = current.facing
                if current.pos == last:
                    break
        disp()
        continue
    print(1000 * (current.pos[0] + 1) + 4 * (current.pos[1] + 1) + current.facing)


def part_2():
    with open(f"../inputs/day_22.txt", "r") as input_file:
        pass


if __name__ == "__main__":
    part_1()
    part_2()
