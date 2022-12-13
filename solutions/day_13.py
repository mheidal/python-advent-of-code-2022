import json
from functools import cmp_to_key
from numpy import sign


def get_ordering(el1, el2) -> int:
    if isinstance(el1, int) and isinstance(el2, int):
        return sign(el1 - el2)
    elif isinstance(el1, list) and isinstance(el2, list):
        min_len = min(len(el1), len(el2))
        for i in range(min_len):
            if (sub_element_ordering := get_ordering(el1[i], el2[i])) != 0:
                return sub_element_ordering
        return sign(len(el1) - len(el2))
    return get_ordering(
        [el1] if isinstance(el1, int) else el1,
        [el2] if isinstance(el2, int) else el2,
    )


def part_1():
    sum_of_correct_indices = 0
    with open(f"../inputs/day_13.txt", "r") as input_file:
        pairs = [[json.loads(packet) for packet in pair.split('\n')] for pair in input_file.read().split("\n\n")]
        for i, pair in enumerate(pairs):
            a, b = pair
            if get_ordering(a, b) == -1:
                sum_of_correct_indices += i + 1
    print(sum_of_correct_indices)


def part_2():
    sentinel_vals = [
        [[2]],
        [[6]]
    ]
    sentinel_product = 1
    with open(f"../inputs/day_13.txt", "r") as input_file:
        lines = [json.loads(line.strip()) for line in input_file.readlines() if line != "\n"]
        lines.extend(sentinel_vals)
        sorted_lines = sorted(lines, key=cmp_to_key(get_ordering))
        for i, line in enumerate(sorted_lines):
            if line in sentinel_vals:
                sentinel_product *= i + 1
    print(sentinel_product)


if __name__ == "__main__":
    part_1()
    part_2()
