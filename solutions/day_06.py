
def find_index_of_unique_character_set(threshold: int) -> int:
    with open(f"../inputs/day_06.txt", 'r') as input_file:
        buf_index = 0
        transmission_index = 0
        buf = [-1] * threshold
        input = input_file.read()
        while len(set(buf)) < threshold or -1 in buf:
            buf[buf_index] = input[transmission_index]
            transmission_index += 1
            buf_index = ((buf_index + 1) % threshold)
        return transmission_index


def part_1():
    print(f"Part 1: {find_index_of_unique_character_set(4)}")
        

def part_2():
    print(f"Part 2: {find_index_of_unique_character_set(14)}")


if __name__ == '__main__':
    part_1()
    part_2()
