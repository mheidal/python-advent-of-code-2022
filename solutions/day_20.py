def part_1():
    with open(f"../inputs/day_20.txt", "r") as input_file:
        file = list(map(int, input_file.readlines()))
        file = [(i, item) for i, item in enumerate(file)]
    order = file.copy()
    for item in order:
        # print([num for i, num in file])
        ix = file.index(item)
        file.remove(item)
        file.insert((ix + item[1]) % len(file), "X")
        file[file.index("X")] = item

    # print([num for i, num in file])
    zero_token = next(i for i in file if i[1] == 0)
    zero = file.index(zero_token)
    grove_coords = [
        file[(zero + 1000) % len(file)][1],
        file[(zero + 2000) % len(file)][1],
        file[(zero + 3000) % len(file)][1],
    ]
    print(grove_coords)
    print(sum(grove_coords))


def part_2():
    with open(f"../inputs/day_20.txt", "r") as input_file:
        file = list(map(lambda x: 811589153 * int(x), input_file.readlines()))
        file = [(i, item) for i, item in enumerate(file)]
    order = file.copy()
    for i in range(10):
        for item in order:
            # print([num for i, num in file])
            ix = file.index(item)
            file.remove(item)
            file.insert((ix + item[1]) % len(file), "X")
            file[file.index("X")] = item

    # print([num for i, num in file])
    zero_token = next(i for i in file if i[1] == 0)
    zero = file.index(zero_token)
    grove_coords = [
        file[(zero + 1000) % len(file)][1],
        file[(zero + 2000) % len(file)][1],
        file[(zero + 3000) % len(file)][1],
    ]
    print(grove_coords)
    print(sum(grove_coords))


if __name__ == "__main__":
    # part_1()
    part_2()
