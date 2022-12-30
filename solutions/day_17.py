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


def let_n_pieces_fall(n: int):

    shapes_index: int = 0
    shapes = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],  # _
        [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # +
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # J
        [(0, 0), (0, 1), (0, 2), (0, 3)],  # |
        [(0, 0), (0, 1), (1, 0), (1, 1)],  # o
    ]
    with open(f"../inputs/day_17.txt", "r") as input_file:
        directions = input_file.read()
    directions_index: int = 0
    occupied_spaces: Set[Tuple[int, int]] = {(i, 0) for i in range(-2, 5)}
    max_height = 0

    previous_starts = {}
    cycle_discovered = False

    i = 0
    while i < n:
        current = copy(shapes[shapes_index])
        shapes_index = (shapes_index + 1) % len(shapes)
        current = add_to_piece(current, (0, max_height + 4))
        this_start_state = (
            tuple(set_from_above(occupied_spaces)),
            shapes_index,
            directions_index,
        )
        if not cycle_discovered and this_start_state in previous_starts:
            cycle_discovered = True
            cycle_start, prev_max_height = previous_starts[this_start_state]
            cycle_len = i - cycle_start
            cycle_height = max_height - prev_max_height
            remaining_complete_cycles = (n - i) // cycle_len
            vertical_offset = cycle_height * remaining_complete_cycles
            max_height += vertical_offset
            occupied_spaces = {
                (space[0], space[1] + vertical_offset) for space in occupied_spaces
            }
            current = add_to_piece(current, (0, vertical_offset))
            i += remaining_complete_cycles * cycle_len
        else:
            previous_starts[this_start_state] = i, max_height
        while True:
            if directions[directions_index] == ">":
                horizontal = add_to_piece(current, (1, 0))
            else:
                horizontal = add_to_piece(current, (-1, 0))

            directions_index = (directions_index + 1) % len(directions)
            if not any([is_out_of_bounds(p) for p in horizontal]) and not any(
                [part in occupied_spaces for part in horizontal]
            ):
                current = horizontal
            lower = add_to_piece(current, (0, -1))
            if any([part[1] < 1 for part in lower]) or any(
                [part in occupied_spaces for part in lower]
            ):
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
                        occupied_spaces = {
                            space for space in occupied_spaces if space[1] >= min_y
                        }
                max_height = max(occupied_spaces, key=lambda x: x[1])[1]
                break
            else:
                current = lower
        i += 1

    print(f"Height after {i} is {max_height}")


def part_1():
    let_n_pieces_fall(2022)


def part_2():
    let_n_pieces_fall(10**12)


if __name__ == "__main__":
    part_1()
    part_2()
