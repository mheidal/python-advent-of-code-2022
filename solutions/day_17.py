from collections import defaultdict
from copy import copy
from typing import Tuple, Set, List, Dict

IntTuple = Tuple[int, int]


def add_to_piece(piece: List[IntTuple], movement: IntTuple):
    new_position = []
    for part in piece:
        new_position.append((part[0] + movement[0], part[1] + movement[1]))
    return new_position


def is_out_of_bounds(piece: IntTuple) -> bool:
    return not (-3 < piece[0] < 5)


def set_from_above(s: Set[IntTuple]) -> List[IntTuple]:
    lst = []
    for i in range(-2, 5):
        subset = {q for q in s if q[0] == i}
        if not subset:
            print("Not enough elements")
            return []
        lst.append(max(subset))
    min_y = min(lst, key=lambda x: x[1])[1]
    for j in range(len(lst)):
        lst[j] = add_to_piece([lst[j]], (0, -1 * min_y))[0]
    return lst


def part_1():
    shapes_index: int = 0
    shapes = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # _
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), ],  # +
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), ],  # J
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # |
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # o
    ]
    with open(f"../inputs/day_17.txt", "r") as input_file:
        directions = input_file.read()
    directions_index: int = 0
    occupied_spaces: Set[Tuple[int, int]] = {(i, 0) for i in range(-2, 5)}
    heights_at_alignments: Dict[int, int] = {}
    max_height = 0
    for i in range(2022):
        current = copy(shapes[shapes_index % len(shapes)])
        shapes_index += 1
        current = add_to_piece(current, (0, max_height + 4))
        while True:
            if directions[directions_index % len(directions)] == ">":
                horizontal = add_to_piece(current, (1, 0))
            else:
                horizontal = add_to_piece(current, (-1, 0))
            directions_index += 1
            if (
                    not any([is_out_of_bounds(p) for p in horizontal])
                    and not any([part in occupied_spaces for part in horizontal])
            ):
                current = horizontal
            lower = add_to_piece(current, (0, -1))
            if any([part[1] < 1 for part in lower]) or any([part in occupied_spaces for part in lower]):
                for part in current:
                    occupied_spaces.add(part)
                # clean up occupied spaces, we only need stuff above the lowest column peak (only so often to minimize
                # cost of cleanup)
                lst = []
                do_trim: bool = True
                if i % 50 == 0:
                    for j in range(-2, 5):
                        subset = {q for q in occupied_spaces if q[0] == j}
                        if not subset:
                            do_trim = False
                        lst.append(max(subset))
                    if do_trim:
                        min_y = min(lst, key=lambda x: x[1])[1]
                        occupied_spaces = {space for space in occupied_spaces if space[1] >= min_y}
                max_height = max(occupied_spaces, key=lambda x: x[1])[1]
                heights_at_alignments[i] = max_height
                break
            else:
                current = lower

    print(f"Height is {max_height}")



def part_2():
    with open(f"../inputs/day_17.txt", "r") as input_file:
        pass


if __name__ == "__main__":
    part_1()
    part_2()
