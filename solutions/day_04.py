class Elf:
    lo: int
    hi: int

    def __init__(self, elf_string):
        lo, hi = elf_string.split("-")
        self.lo = int(lo)
        self.hi = int(hi)


def check_full_containment(elf_1: Elf, elf_2: Elf):
    return (elf_1.lo <= elf_2.lo and elf_2.hi <= elf_1.hi) or (
        elf_2.lo <= elf_1.lo and elf_1.hi <= elf_2.hi
    )


def check_intersect(elf_1: Elf, elf_2: Elf):
    return (elf_1.lo <= elf_2.lo <= elf_1.hi) or (elf_2.lo <= elf_1.lo <= elf_2.hi)


def get_count(checking_function):
    num = 0
    with open(f"../inputs/day_04.txt", "r") as input_file:
        for line in input_file.readlines():
            elf_1, elf_2 = (Elf(elf_string) for elf_string in line.split(","))
            if checking_function(elf_1, elf_2):
                num += 1
    return num


def part_1():
    num = get_count(check_full_containment)
    print(num)


def part_2():
    num = get_count(check_intersect)
    print(num)


if __name__ == "__main__":
    part_1()
    part_2()
