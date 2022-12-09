def get_elves():
    elves = []
    x = open("input.txt", "r").read()
    for line in x.split("\n\n"):
        elf = 0
        for l in line.split("\n"):
            elf += int(l)
        elves.append(elf)
    return elves


def part_1():
    elves = get_elves()
    print(max(elves))


def part_2():
    elves = get_elves()
    print(sum(sorted(elves)[-3:]))


if __name__ == "__main__":
    part_1()
    part_2()
