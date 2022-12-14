import re
from typing import List, Tuple


def get_grid(include_buffers: bool) -> Tuple[List[List[bool]], int, int]:
    with open(f"../inputs/day_14.txt", "r") as input_file:
        input_text = input_file.read()
        all_coords = [[int(c) for c in coord.split(',')] for coord in re.findall(r"\d+,\d+", input_text)]
        all_coords.append([500, 0])
        min_x = min(all_coords, key=lambda c: c[0])[0]
        min_y = min(all_coords, key=lambda c: c[1])[1]
        max_x = max(all_coords, key=lambda c: c[0])[0]
        max_y = max(all_coords, key=lambda c: c[1])[1]
        if include_buffers:
            max_y += 2
            min_x -= 2 * max_y
            max_x += 2 * max_y
            input_text += f"\n{min_x},{max_y} -> {max_x},{max_y}"

        grid = []
        for i in range(min_y, max_y+1):
            grid.append([False] * (max_x + 1 - min_x))

        for line in input_text.splitlines():
            corner_points = [corner_point for corner_point in line.split(" -> ")]
            for i in range(len(corner_points) - 1):
                x1, y1 = [int(c) for c in corner_points[i].split(',')]
                x1 -= min_x
                y1 -= min_y
                x2, y2 = [int(c) for c in corner_points[i + 1].split(',')]
                x2 -= min_x
                y2 -= min_y
                if x1 == x2:
                    for row in grid[min(y1,y2):max(y1,y2) + 1]:
                        row[x1] = True
                else:
                    grid[y1][min(x1,x2):max(x1,x2) + 1] = [True] * (abs(x2 - x1)+1)

    return grid, min_x, min_y


def insert_sand_grain_worked(grid:List[List[bool]], x_offset, y_offset):
    """Mutates grid, trying to insert a sand grain/settle it. Returns whether the sand grain could be inserted."""
    pos_x, pos_y = 500 - x_offset, 0 - y_offset
    if grid[pos_y][pos_x]:
        return False
    has_next = True
    while has_next:
        if pos_y == len(grid) - 1:
            return False
        if not grid[pos_y+1][pos_x]:
            pos_y += 1
        elif pos_x > 0 and not grid[pos_y+1][pos_x-1]:
            pos_y += 1
            pos_x -= 1
        elif pos_x < len(grid[0]) - 1 and not grid[pos_y+1][pos_x+1]:
            if pos_x == len(grid[0]) - 1:
                return False
            pos_y += 1
            pos_x += 1
        else:
            if (
                (pos_x == 0 and pos_y < len(grid) - 1 and grid[pos_y+1][pos_x])
                or (pos_x == len(grid[0]) - 1 and pos_y < len(grid) - 1 and grid[pos_y+1][pos_x] and grid[pos_y+1][pos_x-1])
            ):
                return False
            else:
                has_next = False
    grid[pos_y][pos_x] = True
    return True


def part_1():
    grid, x_offset, y_offset = get_grid(False)
    sand_grains = 0
    while insert_sand_grain_worked(grid, x_offset, y_offset):
        sand_grains += 1
    print(sand_grains)


def part_2():
    grid, x_offset, y_offset = get_grid(True)
    sand_grains = 0
    while insert_sand_grain_worked(grid, x_offset, y_offset):
        sand_grains += 1
    print(sand_grains)


if __name__ == "__main__":
    part_1()
    part_2()
