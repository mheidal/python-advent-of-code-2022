from typing import List


def one_at_a_time(stacks, move_number, origin_index, destination_index):
    for _ in range(move_number):
        stacks[destination_index].append(stacks[destination_index].pop())


def all_at_once(stacks, move_number, origin_index, destination_index):
    crates = stacks[origin_index][-move_number:]
    stacks[origin_index] = stacks[origin_index][:-move_number]
    stacks[destination_index].extend(crates)


def rearrange_crates(modification_strategy):
    with open(f"../inputs/day_05.txt", "r") as input_file:
        stacks: List[List[str]] = [[] for _ in range(9)]
        crate_section, movement_section = input_file.read().split("\n\n")
        for crate_line in crate_section.split("\n"):
            if "1" not in crate_line:
                for i, char in enumerate(crate_line):
                    if i % 4 == 1 and not char == " ":
                        stacks[i // 4].insert(0, char)
        for movement_line in movement_section.split("\n"):
            _, move_number, _, origin_index, _, destination_index = movement_line.split(
                " "
            )
            move_number = int(move_number)
            origin_index = int(origin_index) - 1
            destination_index = int(destination_index) - 1
            modification_strategy(stacks, move_number, origin_index, destination_index)
        tops = "".join(stack.pop() if stack else "💀" for stack in stacks)
        print(tops)


def part_1():
    rearrange_crates(one_at_a_time)


def part_2():
    rearrange_crates(all_at_once)


if __name__ == "__main__":
    part_1()
    part_2()
