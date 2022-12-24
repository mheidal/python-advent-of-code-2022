from enum import IntEnum
from typing import List, Tuple, Dict
import re

Grid = List[List[str]]
CoordId = Tuple[int, int]


class Facing(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class Coord:
    def __init__(self, right: CoordId, down: CoordId, left: CoordId, up: CoordId):
        self.right = right
        self.down = down
        self.left = left
        self.up = up

    def go(self, facing: Facing) -> CoordId:
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
        if coord != ' ':
            return i
    raise ValueError


def get_index_of_rightmost_coord(grid: Grid, row_index: int) -> int:
    row = grid[row_index]
    for i, coord in reversed(list(enumerate(row))):
        if coord != ' ':
            return i
    raise ValueError


def get_index_of_lowest_coord(grid: Grid, col_index: int) -> int:
    col = [row[col_index] for row in grid]
    for i, coord in reversed(list(enumerate(col))):
        if coord != ' ':
            return i
    raise ValueError


def get_index_of_highest_coord(grid: Grid, col_index: int) -> int:
    col = [row[col_index] for row in grid]
    for i, coord in enumerate(col):
        if coord != ' ':
            return i
    raise ValueError


def is_valid_position(grid, row_index, col_index):
    return (
        -1 < row_index < len(grid)
        and -1 < col_index < len(grid[0])
    )


def part_1():
    with open(f"../inputs/day_22.txt", "r") as input_file:
        grid_section, directions_section = input_file.read().split("\n\n")
    grid = [list(line) for line in grid_section.split('\n')]
    coords: Dict[CoordId, Coord] = {}
    for row_index, row in enumerate(grid):
        for col_index, entry in enumerate(row):
            if entry != ' ':
                positions: List[Tuple[int, int]] = [(-1, -1)] * 4  # r, d, l, u

                # Right
                if is_valid_position(grid, row_index, col_index + 1) and grid[row_index][col_index + 1] != ' ':
                    positions[0] = (row_index, col_index + 1)
                else:
                    positions[0] = (row_index, get_index_of_leftmost_coord(grid, row_index))

                # Down
                if is_valid_position(grid, row_index + 1, col_index) and grid[row_index + 1][col_index] != ' ':
                    positions[1] = (row_index + 1, col_index)
                else:
                    positions[1] = (get_index_of_highest_coord(grid, col_index), col_index)

                # Left
                if is_valid_position(grid, row_index, col_index - 1) and grid[row_index][col_index - 1] != ' ':
                    positions[2] = (row_index, col_index - 1)
                else:
                    positions[2] = (row_index, get_index_of_rightmost_coord(grid, row_index))

                # Up
                if is_valid_position(grid, row_index - 1, col_index) and grid[row_index - 1][col_index] != ' ':
                    positions[3] = (row_index - 1, col_index)
                else:
                    positions[3] = (get_index_of_lowest_coord(grid, col_index), col_index)

                for action, coord in enumerate(positions):
                    i, j = coord
                    if grid[i][j] == "#":
                        positions[action] = (row_index, col_index)

                coords[(row_index, col_index)] = Coord(*positions)

    directions = re.findall("\\D+|\\d+", directions_section)

    facing = Facing.RIGHT
    position: CoordId = (0, get_index_of_leftmost_coord(grid, 0))
    
    def disp():
        for i, row in enumerate(grid):
            s = ""
            for j, entry in enumerate(row):
                if (i, j) == position:
                    if facing == Facing.RIGHT:
                        s += ">"
                    elif facing == Facing.DOWN:
                        s += "v"
                    elif facing == Facing.LEFT:
                        s += "<"
                    else:
                        s += "^"
                else:
                    s += entry
            print(s)
        print()
    # disp()
    for action in directions:
        if action in "LR":
            facing = get_turn_direction(action, facing)
        else:
            for _ in range(int(action)):
                next_position = coords[position].go(facing)
                position = next_position
        # disp()
    print(1000 * (position[0] + 1) + 4 * (position[1] + 1) + facing)


def part_2():
    with open(f"../inputs/day_22.txt", "r") as input_file:
        pass


if __name__ == "__main__":
    part_1()
    part_2()
