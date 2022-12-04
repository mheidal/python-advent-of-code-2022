

def get_priority(item: str) -> int:
    if (ascii_val := ord(item)) >= 97:
        return ascii_val - 96  # lowercase
    return ascii_val - 38  # uppercase


def part_1():
    with open(f"../inputs/day_03.txt", 'r') as input_file:
        summed_priorities = 0
        for line in input_file.readlines():
            first_compartment = line[:len(line)//2]
            second_compartment = line[len(line)//2:]
            for item in set(first_compartment):
                if item in set(second_compartment):
                    summed_priorities += get_priority(item)
        print(f"Part 1: {summed_priorities}")


def part_2():
    with open(f"../inputs/day_03.txt", 'r') as input_file:
        summed_priorities = 0
        elves = input_file.readlines()
        for line_triplet in range(0, len(elves), 3):
            triplet = []
            for triplet_index in range(3):
                triplet.append(set(elves[line_triplet + triplet_index].strip()))
            for item in triplet[0]:
                if item in triplet[1] and item in triplet[2]:
                    summed_priorities += get_priority(item)
        print(f"Part 2: {summed_priorities}")


if __name__ == '__main__':
    part_1()
    part_2()
