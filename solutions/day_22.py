from enum import IntEnum, Enum
from typing import List, Tuple, Dict, NamedTuple, Callable, Union
import re

Grid = List[List[str]]


class CoordId(NamedTuple):
    row: int
    col: int


class Facing(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    NOTSET = -1


class Edge(NamedTuple):
    pos: CoordId
    focused: Facing


class Corner(Enum):
    CONVEX = 0
    CONCAVE = 1
    FLAT = 2


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
    if -1 < row_index < len(grid) and -1 < col_index < len(grid[0]):
        return grid[row_index][col_index] != " "
    return False


def get_mapping_wrapping(grid: Grid) -> Dict[CoordId, Coord]:
    coords: Dict[CoordId, Coord] = {}
    for row_index, row in enumerate(grid):
        for col_index, entry in enumerate(row):
            if entry != " ":
                positions: List[Result] = [
                    Result(CoordId(-1, -1), Facing.NOTSET)
                ] * 4  # r, d, l, u

                # Right
                if is_valid_position(grid, row_index, col_index + 1):
                    positions[0] = Result(
                        CoordId(row_index, col_index + 1), Facing.RIGHT
                    )
                else:
                    positions[0] = Result(
                        CoordId(
                            row_index, get_index_of_leftmost_coord(grid, row_index)
                        ),
                        Facing.RIGHT,
                    )

                # Down
                if is_valid_position(grid, row_index + 1, col_index):
                    positions[1] = Result(
                        CoordId(row_index + 1, col_index), Facing.DOWN
                    )
                else:
                    positions[1] = Result(
                        CoordId(get_index_of_highest_coord(grid, col_index), col_index),
                        Facing.DOWN,
                    )

                # Left
                if is_valid_position(grid, row_index, col_index - 1):
                    positions[2] = Result(
                        CoordId(row_index, col_index - 1), Facing.LEFT
                    )
                else:
                    positions[2] = Result(
                        CoordId(
                            row_index, get_index_of_rightmost_coord(grid, row_index)
                        ),
                        Facing.LEFT,
                    )

                # Up
                if is_valid_position(grid, row_index - 1, col_index):
                    positions[3] = Result(CoordId(row_index - 1, col_index), Facing.UP)
                else:
                    positions[3] = Result(
                        CoordId(get_index_of_lowest_coord(grid, col_index), col_index),
                        Facing.UP,
                    )

                # Check each to ensure it doesn't lead into a blocker
                for action, result in enumerate(positions):
                    i, j = result.pos
                    if grid[i][j] == "#":
                        positions[action] = Result(
                            CoordId(row_index, col_index), result.facing
                        )

                coords[CoordId(row_index, col_index)] = Coord(*positions)
    return coords


def get_ccw_piece(piece: Edge, grid: Grid) -> Tuple[Edge, Corner]:
    row, col = piece.pos

    # names of coord ids in each of the eight directions for convenience
    # left, up left, down left, etc (names standardized to two letters)
    ll = CoordId(row, col - 1)
    ul = CoordId(row - 1, col - 1)
    dl = CoordId(row + 1, col - 1)
    uu = CoordId(row - 1, col)
    dd = CoordId(row + 1, col)
    rr = CoordId(row, col + 1)
    ur = CoordId(row - 1, col + 1)
    dr = CoordId(row + 1, col + 1)

    if piece.focused == Facing.UP:
        if is_valid_position(grid, *ll):
            if not is_valid_position(grid, *ul):
                return Edge(ll, piece.focused), Corner.FLAT
            else:
                return Edge(ul, Facing.RIGHT), Corner.CONCAVE
        else:
            return Edge(piece.pos, Facing.LEFT), Corner.CONVEX
    elif piece.focused == Facing.RIGHT:
        if is_valid_position(grid, *uu):
            if not is_valid_position(grid, *ur):
                return Edge(uu, piece.focused), Corner.FLAT
            else:
                return Edge(ur, Facing.DOWN), Corner.CONCAVE
        else:
            return Edge(piece.pos, Facing.UP), Corner.CONVEX
    elif piece.focused == Facing.DOWN:
        if is_valid_position(grid, *rr):
            if not is_valid_position(grid, *dr):
                return Edge(rr, piece.focused), Corner.FLAT
            else:
                return Edge(dr, Facing.LEFT), Corner.CONCAVE
        else:
            return Edge(piece.pos, Facing.RIGHT), Corner.CONVEX
    elif piece.focused == Facing.LEFT:
        if is_valid_position(grid, *dd):
            if not is_valid_position(grid, *dl):
                return Edge(dd, piece.focused), Corner.FLAT
            else:
                return Edge(dl, Facing.UP), Corner.CONCAVE
        else:
            return Edge(piece.pos, Facing.DOWN), Corner.CONVEX
    raise ValueError


def get_other_in_mapping(
    coord: CoordId, desired_facing: Facing, mappings: List[Tuple[Edge, Edge]]
):
    mapping = next(
        mapping
        for mapping in mappings
        if any([e.pos == coord and e.focused == desired_facing for e in mapping])
    )
    return mapping[0] if mapping[0].pos != coord else mapping[1]


def get_mapping_folding(grid: Grid):
    key_edge_piece: Union[CoordId, None] = None
    coords: Dict[CoordId, Coord] = {}
    saved_for_later = []
    for row_index, row in enumerate(grid):
        for col_index, entry in enumerate(row):
            if entry != " ":
                positions: List[Result] = [
                    Result(CoordId(-1, -1), Facing.NOTSET)
                ] * 4  # r, d, l, u

                # Right
                if is_valid_position(grid, row_index, col_index + 1):
                    positions[0] = Result(
                        CoordId(row_index, col_index + 1), Facing.RIGHT
                    )
                else:
                    if not key_edge_piece:
                        key_edge_piece = CoordId(row_index, col_index)
                    saved_for_later.append(CoordId(row_index, col_index))
                    continue

                # Down
                if is_valid_position(grid, row_index + 1, col_index):
                    positions[1] = Result(
                        CoordId(row_index + 1, col_index), Facing.DOWN
                    )
                else:
                    if not key_edge_piece:
                        key_edge_piece = CoordId(row_index, col_index)
                    saved_for_later.append(CoordId(row_index, col_index))
                    continue

                # Left
                if is_valid_position(grid, row_index, col_index - 1):
                    positions[2] = Result(
                        CoordId(row_index, col_index - 1), Facing.LEFT
                    )
                else:
                    if not key_edge_piece:
                        key_edge_piece = CoordId(row_index, col_index)
                    saved_for_later.append(CoordId(row_index, col_index))
                    continue

                # Up
                if is_valid_position(grid, row_index - 1, col_index):
                    positions[3] = Result(CoordId(row_index - 1, col_index), Facing.UP)
                else:
                    if not key_edge_piece:
                        key_edge_piece = CoordId(row_index, col_index)
                    saved_for_later.append(CoordId(row_index, col_index))
                    continue

                # Check each to ensure it doesn't lead into a blocker
                for action, result in enumerate(positions):
                    i, j = result.pos
                    if grid[i][j] == "#":
                        positions[action] = Result(
                            CoordId(row_index, col_index), result.facing
                        )

                coords[CoordId(row_index, col_index)] = Coord(*positions)

    assert key_edge_piece
    kep_facing: Union[None, Facing] = None
    kep_row, kep_col = key_edge_piece
    if not is_valid_position(grid, kep_row - 1, kep_col):
        kep_facing = Facing.UP
    elif not is_valid_position(grid, kep_row, kep_col - 1):
        kep_facing = Facing.LEFT
    elif not is_valid_position(grid, kep_row + 1, kep_col):
        kep_facing = Facing.DOWN
    elif not is_valid_position(grid, kep_row, kep_col + 1):
        kep_facing = Facing.RIGHT
    assert kep_facing
    edge_pieces: List[Union[Corner, Edge]] = [Edge(key_edge_piece, kep_facing)]
    loop_incomplete = True
    while loop_incomplete:
        ccw, corner_type = get_ccw_piece(edge_pieces[0], grid)
        if ccw in edge_pieces:
            loop_incomplete = False
        else:
            if corner_type != Corner.FLAT:
                edge_pieces.insert(0, corner_type)
            edge_pieces.insert(0, ccw)
    mappings: List[Tuple[Edge, Edge]] = []
    alphanums = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcedfghijklmnopqrstuvwxyz0123456789"

    def disp():
        s = ""
        for row_index, row in enumerate(grid):
            for col_index, entry in enumerate(row):
                enny = False
                for mapping_index, mapping in enumerate(mappings):
                    if not enny:
                        if mapping[0].pos == (row_index, col_index) or mapping[
                            1
                        ].pos == (row_index, col_index):
                            enny = True
                            s += alphanums[mapping_index]
                if not enny:
                    s += grid[row_index][col_index]
            s += "\n"
        print(s)

    queue: List[Tuple[int, int]] = [
        (i - 1, i + 1) for i, piece in enumerate(edge_pieces) if piece == Corner.CONCAVE
    ]
    while queue:
        ccw_index, cw_index = queue.pop(0)
        ccw_index %= len(edge_pieces)
        cw_index %= len(edge_pieces)
        ccw, cw = edge_pieces[ccw_index], edge_pieces[cw_index]
        if ccw == Corner.CONVEX and cw == Corner.CONVEX:
            continue
        else:
            if ccw == Corner.CONVEX:
                ccw_index -= 1
                ccw_index %= len(edge_pieces)
                ccw = edge_pieces[ccw_index]
            elif cw == Corner.CONVEX:
                cw_index += 1
                cw_index %= len(edge_pieces)
                cw = edge_pieces[cw_index]
            if not any(
                [e1 == ccw or e2 == ccw or e1 == cw or e2 == cw for e1, e2 in mappings]
            ):
                mappings.append((ccw, cw))
            # disp()
            queue.append((ccw_index - 1, cw_index + 1))

    reversed_facings = {
        Facing.UP: Facing.DOWN,
        Facing.RIGHT: Facing.LEFT,
        Facing.DOWN: Facing.UP,
        Facing.LEFT: Facing.RIGHT,
    }

    for coord in saved_for_later:
        row_index, col_index = coord
        positions: List[Result] = [
            Result(CoordId(-1, -1), Facing.NOTSET)
        ] * 4  # r, d, l, u
        # Right
        if is_valid_position(grid, row_index, col_index + 1):
            positions[0] = Result(CoordId(row_index, col_index + 1), Facing.RIGHT)
        else:
            other = get_other_in_mapping(coord, Facing.RIGHT, mappings)
            positions[0] = Result(other.pos, reversed_facings[other.focused])

        # Down
        if is_valid_position(grid, row_index + 1, col_index):
            positions[1] = Result(CoordId(row_index + 1, col_index), Facing.DOWN)
        else:
            other = get_other_in_mapping(coord, Facing.DOWN, mappings)
            positions[1] = Result(other.pos, reversed_facings[other.focused])

        # Left
        if is_valid_position(grid, row_index, col_index - 1):
            positions[2] = Result(CoordId(row_index, col_index - 1), Facing.LEFT)
        else:
            other = get_other_in_mapping(coord, Facing.LEFT, mappings)
            positions[2] = Result(other.pos, reversed_facings[other.focused])

        # Up
        if is_valid_position(grid, row_index - 1, col_index):
            positions[3] = Result(CoordId(row_index - 1, col_index), Facing.UP)
        else:
            other = get_other_in_mapping(coord, Facing.UP, mappings)
            positions[3] = Result(other.pos, reversed_facings[other.focused])

        # Check each to ensure it doesn't lead into a blocker
        for action, result in enumerate(positions):
            if grid[result.pos.row][result.pos.col] == "#":
                facing = {
                    0: Facing.RIGHT,
                    1: Facing.DOWN,
                    2: Facing.LEFT,
                    3: Facing.UP,
                }[action]
                positions[action] = Result(coord, facing)
        coords[coord] = Coord(*positions)

    return coords


def do_traversal(mapping_func: Callable[[Grid], Dict[CoordId, Coord]]) -> int:

    with open(f"../inputs/day_22.txt", "r") as input_file:
        grid_section, directions_section = input_file.read().split("\n\n")
    grid = [list(line) for line in grid_section.split("\n")]
    coords = mapping_func(grid)
    directions = re.findall("\\D+|\\d+", directions_section)
    current = Result(CoordId(0, get_index_of_leftmost_coord(grid, 0)), Facing.RIGHT)
    hist: Dict[CoordId, Facing] = {current.pos: current.facing}

    def disp():
        s = ""
        for row_index, row in enumerate(grid):
            for col_index, entry in enumerate(row):
                if (pos := CoordId(row_index, col_index)) in hist:
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
        # disp()
    return 1000 * (current.pos[0] + 1) + 4 * (current.pos[1] + 1) + current.facing


def part_1():
    score = do_traversal(get_mapping_wrapping)
    print(f"Part 1: {score}")


def part_2():
    score = do_traversal(get_mapping_folding)
    print(f"Part 2: {score}")


if __name__ == "__main__":
    # part_1()
    part_2()
