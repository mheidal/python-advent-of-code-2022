
def find_index_of_unique_character_set(threshold: int) -> int:
    with open(f"../inputs/day_06.txt", 'r') as input_file:
        input = input_file.read()
        for i in range(threshold, len(input), 1):
            if len(set(input[i-threshold:i])) == threshold:
                return i
    return -1


def part_1():
    print(f"Part 1: {find_index_of_unique_character_set(4)}")
        

def part_2():
    print(f"Part 2: {find_index_of_unique_character_set(14)}")


if __name__ == '__main__':
    part_1()
    part_2()
