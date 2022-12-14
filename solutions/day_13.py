import json
from functools import cmp_to_key
from typing import Union
from numpy import sign


def get_ordering(element_1: Union[list, int], element_2: Union[list, int]) -> int:
    if isinstance(element_1, int) and isinstance(element_2, int):
        return sign(element_1 - element_2)
    elif isinstance(element_1, list) and isinstance(element_2, list):
        min_len = min(len(element_1), len(element_2))
        for i in range(min_len):
            if (sub_element_ordering := get_ordering(element_1[i], element_2[i])) != 0:
                return sub_element_ordering
        return sign(len(element_1) - len(element_2))
    return get_ordering(
        [element_1] if isinstance(element_1, int) else element_1,
        [element_2] if isinstance(element_2, int) else element_2,
    )


def part_1():
    sum_of_correct_indices = 0
    with open(f"../inputs/day_13.txt", "r") as input_file:
        pairs = [
            [json.loads(packet) for packet in pair.split("\n")]
            for pair in input_file.read().split("\n\n")
        ]
        for i, pair in enumerate(pairs):
            a, b = pair
            if get_ordering(a, b) == -1:
                sum_of_correct_indices += i + 1
    print(sum_of_correct_indices)


def part_2():
    sentinel_vals = [[[2]], [[6]]]
    sentinel_product = 1
    with open(f"../inputs/day_13.txt", "r") as input_file:
        lines = [
            json.loads(line.strip()) for line in input_file.readlines() if line != "\n"
        ]
        lines.extend(sentinel_vals)
        sorted_lines = sorted(lines, key=cmp_to_key(get_ordering))
        for i, line in enumerate(sorted_lines):
            if line in sentinel_vals:
                sentinel_product *= i + 1
    print(sentinel_product)


if __name__ == "__main__":
    part_1()
    part_2()
