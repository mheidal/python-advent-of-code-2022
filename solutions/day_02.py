
def get_points_for_match(them, you):
    matchups = {
        "R": {
            "R": 3,
            "P": 6,
            "S": 0,
        },
        "P": {
            "R": 0,
            "P": 3,
            "S": 6,
        },
        "S": {
            "R": 6,
            "P": 0,
            "S": 3,
        },
    }
    return matchups[them][you]


def get_shapes_1(line: str):
    letter_to_shape = {
        "A": "R",
        "B": "P",
        "C": "S",
        "X": "R",
        "Y": "P",
        "Z": "S",
    }
    them, you = line.strip().split(' ')
    return letter_to_shape[them], letter_to_shape[you]

def get_shapes_2(line: str):
    letter_to_shape = {
        "A": "R",
        "B": "P",
        "C": "S",
    }
    shape_and_strat_to_shape = {
        "R": {
            "X": "S",
            "Y": "R",
            "Z": "P"
        },
        "P": {
            "X": "R",
            "Y": "P",
            "Z": "S"
        },
        "S": {
            "X": "P",
            "Y": "S",
            "Z": "R"
        },
    }
    them, you = line.strip().split(' ')
    them_shape = letter_to_shape[them]
    return them_shape, shape_and_strat_to_shape[them_shape][you]


def get_points_for_game(strat_func):

    points_for_choice = {
        "R": 1,
        "P": 2,
        "S": 3,
    }
    with open(f"../inputs/day_02.txt", 'r') as input_file:
        sum = 0
        for line in input_file.readlines():
            them, you = strat_func(line)
            sum += get_points_for_match(them, you)
            sum += points_for_choice[you]
        print(sum)


def part_1():
    get_points_for_game(get_shapes_1)


def part_2():
    get_points_for_game(get_shapes_2)
        
        
if __name__ == '__main__':
    part_1()
    part_2()
