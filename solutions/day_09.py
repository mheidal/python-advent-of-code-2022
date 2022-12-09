from typing import List, Tuple


def add_tuples(first: Tuple[int, int], second: Tuple[int, int]) -> Tuple[int, int]:
    """Returns a list where the nth element is the sum of the nth elements of lists a and b."""
    return first[0] + second[0], first[1] + second[1]


def get_required_motion(leader: Tuple[int, int], follower: Tuple[int, int]) -> Tuple[int, int]:
    x_diff = follower[0] - leader[0]
    y_diff = follower[1] - leader[1]
    if x_diff == 0:
        if y_diff < -1:   # follow up
            return 0, 1
        elif y_diff > 1:  # follow down
            return 0, -1
    elif y_diff == 0:
        if x_diff < -1:  # follow right
            return 1, 0
        elif x_diff > 1:  # follow left
            return -1, 0
    elif x_diff != 0 and y_diff != 0 and (abs(x_diff) > 1 or abs(y_diff) > 1):
        if x_diff < 0:  # L
            if y_diff < 0:  # LU
                return 1, 1
            elif y_diff > 0:  # LD
                return 1, -1
        elif x_diff > 0:  # R
            if y_diff < 0:  # RU
                return -1, 1
            elif y_diff > 0:  # RD
                return -1, -1
    return 0, 0

def calculate_knot_positions(rope_len: int):
    knots = [(0, 0) for _ in range(rope_len)]
    knot_position_histories = [{knot} for knot in knots]
    directions = {
        'U': (0, 1),
        'L': (-1, 0),
        "R": (1, 0),
        "D": (0, -1)
    }
    with open(f"../inputs/day_09.txt", 'r') as input_file:
        for line in input_file.readlines():
            direc, dist = line.strip().split(" ")
            for _ in range(int(dist)):
                knots[0] = add_tuples(knots[0], directions[direc])
                for i in range(0, rope_len-1):
                    trailing_movement = get_required_motion(knots[i], knots[i + 1])
                    knots[i+1] = add_tuples(knots[i+1], trailing_movement)
                    knot_position_histories[i + 1].add(tuple(knots[i + 1]))
    return knot_position_histories


def part_1():
    knot_position_histories = calculate_knot_positions(2)
    print(len(knot_position_histories[1]))


def part_2():
    knot_position_histories = calculate_knot_positions(10)
    print(len(knot_position_histories[9]))


if __name__ == '__main__':
    part_1()
    part_2()
