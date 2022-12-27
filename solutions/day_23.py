from typing import Tuple, List, Dict, Any, Callable

Self = Any


def group_has_elf(group, all_elves) -> bool:
    elf_found = False
    for pos in group:
        if pos in all_elves:
            elf_found = True
    return elf_found


def get_full_adjacent(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    adjs = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                adjs.append((pos[0] + i, pos[1] + j))
    return adjs


def get_north_mvmt(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (pos[0] - 1, pos[1] - 1),
        (pos[0] + 0, pos[1] - 1),
        (pos[0] + 1, pos[1] - 1),
    ]


def get_south_mvmt(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (pos[0] - 1, pos[1] + 1),
        (pos[0] + 0, pos[1] + 1),
        (pos[0] + 1, pos[1] + 1),
    ]


def get_west_mvmt(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (pos[0] - 1, pos[1] - 1),
        (pos[0] - 1, pos[1] + 0),
        (pos[0] - 1, pos[1] + 1),
    ]


def get_east_mvmt(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [
        (pos[0] + 1, pos[1] - 1),
        (pos[0] + 1, pos[1] + 0),
        (pos[0] + 1, pos[1] + 1),
    ]


class Elf:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.proposed = None
        self.must_move = True

    def set_proposed_movement(
        self,
        all_elves: Dict[Tuple[int, int], Self],
        movements_offset: int,
    ) -> None:
        """all_elves is a dict of elf coords to Elf objects. Any is a standin for Self here."""
        movements: List[Callable[[Tuple[int, int]], List[Tuple[int, int]]]] = [
            get_north_mvmt,
            get_south_mvmt,
            get_west_mvmt,
            get_east_mvmt,
        ]

        movements_to_proposed: Dict[
            Callable[[Tuple[int, int]], List[Tuple[int, int]]], Tuple[int, int]
        ] = {
            get_north_mvmt: (self.x, self.y - 1),
            get_south_mvmt: (self.x, self.y + 1),
            get_west_mvmt: (self.x - 1, self.y),
            get_east_mvmt: (self.x + 1, self.y),
        }

        pos = (self.x, self.y)
        if not group_has_elf(get_full_adjacent(pos), all_elves):
            self.proposed = None
            self.must_move = False
        elif not group_has_elf(
            (mvmt := movements[(0 + movements_offset) % len(movements)])(pos), all_elves
        ):
            self.proposed = movements_to_proposed[mvmt]
        elif not group_has_elf(
            (mvmt := movements[(1 + movements_offset) % len(movements)])(pos), all_elves
        ):
            self.proposed = movements_to_proposed[mvmt]
        elif not group_has_elf(
            (mvmt := movements[(2 + movements_offset) % len(movements)])(pos), all_elves
        ):
            self.proposed = movements_to_proposed[mvmt]
        elif not group_has_elf(
            (mvmt := movements[(3 + movements_offset) % len(movements)])(pos), all_elves
        ):
            self.proposed = movements_to_proposed[mvmt]
        else:
            self.proposed = None
            self.must_move = False


def parts_1_and_2():
    elves: Dict[Tuple[int, int], Elf] = {}
    with open(f"../inputs/day_23.txt", "r") as input_file:
        for row_index, row in enumerate(input_file.readlines()):
            for col_index, entry in enumerate(row):
                if entry == "#":
                    elves[(col_index, row_index)] = Elf(col_index, row_index)
    any_elf_has_proposed_movement = True
    movement_offset = 0
    round = 0
    while True:
        if round % 10 == 0:
            print(round)
        # stage 1: targeting
        for pos, elf in elves.items():
            elf.set_proposed_movement(elves, movement_offset)

        # stage 2: moving
        if not any([elf.must_move for elf in elves.values()]):
            print(f"Part 2: {round+1}")
            break
        new_elves: Dict[Tuple[int, int], Elf] = {}
        for elf in elves.values():
            if elf.proposed is None or any(
                [e.proposed == elf.proposed and e is not elf for e in elves.values()]
            ):
                new_elves[(elf.x, elf.y)] = Elf(elf.x, elf.y)
            else:
                new_elves[elf.proposed] = Elf(*elf.proposed)

        # draw_elves(new_elves)
        elves = new_elves
        round += 1
        if round == 10:
            minx = min(elves.keys(), key=lambda x: x[0])[0]
            maxx = max(elves.keys(), key=lambda x: x[0])[0] + 1
            miny = min(elves.keys(), key=lambda x: x[1])[1]
            maxy = max(elves.keys(), key=lambda x: x[1])[1] + 1
            print(f"Part 1: {(maxx - minx) * (maxy - miny) - len(elves)}")
        movement_offset = (movement_offset + 1) % 4


if __name__ == "__main__":
    parts_1_and_2()
