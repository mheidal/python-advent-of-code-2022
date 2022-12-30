def snafu_to_dec(s: str) -> int:
    values = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    num = 0
    exponent = 1
    while s:
        last = s[-1]
        s = s[:-1]
        num += exponent * values[last]
        exponent *= 5
    return num


def dec_to_snafu(dec: int) -> str:
    pental_digits = []
    s = ""
    mappings = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-", 5: "0"}
    while dec:
        pental_digits.append(dec % 5)
        dec //= 5
    pental_digits.append(0)
    for i, digit in enumerate(pental_digits):
        if i == len(pental_digits) - 1 and digit == 0:
            continue
        s += mappings[digit]
        if digit > 2:
            pental_digits[i + 1] += 1
    return s[::-1]


def part_1():
    val = 0
    with open(f"../inputs/day_25.txt", "r") as input_file:
        for line in input_file.read().splitlines():
            val += snafu_to_dec(line)
    print(dec_to_snafu(val))


if __name__ == "__main__":
    part_1()
