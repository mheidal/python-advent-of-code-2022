from typing import Tuple


def cardinal_adjacent(droplet: Tuple[int, int, int]):
    return [
        (droplet[0] + 1, droplet[1], droplet[2]),
        (droplet[0] - 1, droplet[1], droplet[2]),
        (droplet[0], droplet[1] + 1, droplet[2]),
        (droplet[0], droplet[1] - 1, droplet[2]),
        (droplet[0], droplet[1], droplet[2] + 1),
        (droplet[0], droplet[1], droplet[2] - 1),
    ]


def full_adjacent(droplet):
    adjacent_cells = []
    for i in range(droplet[0] - 1, droplet[0] + 2):
        for j in range(droplet[1] - 1, droplet[1] + 2):
            for k in range(droplet[2] - 1, droplet[2] + 2):
                adjacent_cells.append((i, j, k))
    adjacent_cells.remove(droplet)
    return adjacent_cells


def part_1():
    count = 0
    droplets = set()
    with open(f"../inputs/day_18.txt", "r") as input_file:
        for line in input_file.readlines():
            droplets.add(tuple(map(int, line.split(","))))
    for droplet in droplets:
        for adj in cardinal_adjacent(droplet):
            if adj not in droplets:
                count += 1
    print(count)


def part_2():
    droplets = set()
    with open(f"../inputs/day_18.txt", "r") as input_file:
        for line in input_file.readlines():
            droplets.add(tuple(map(int, line.split(","))))

    # top droplet haha
    toplet = max(droplets, key=lambda droplet: droplet[1])
    toplet = (toplet[0], toplet[1] + 1, toplet[2])

    skin = set()
    queue = [toplet]
    while queue:
        cell = queue.pop()
        skin.add(cell)
        for possible_skin_cell in cardinal_adjacent(cell):
            if possible_skin_cell not in skin and possible_skin_cell not in droplets:
                if any(
                    [
                        further_adjacent in droplets
                        for further_adjacent in full_adjacent(possible_skin_cell)
                    ]
                ):
                    queue.append(possible_skin_cell)

    count = 0
    for droplet in droplets:
        for possible_skin_cell in cardinal_adjacent(droplet):
            if possible_skin_cell in skin:
                count += 1
    print(count)


if __name__ == "__main__":
    part_1()
    part_2()
