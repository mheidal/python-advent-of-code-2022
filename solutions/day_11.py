from typing import List
from math import lcm
import re


class Monkey:
    monkeys = []
    master_divisor: int = None

    def __init__(self, items: List[int], div_test: int, operation, id: int, true: int, false: int, div_by_three: bool = True):
        self.id = id
        self.inspect_count = 0
        self.items = items
        self.div_test = div_test
        self.operation = operation
        self.true = true
        self.false = false
        self.div_by_three = div_by_three
        Monkey.monkeys.append(self)

    def take_turn(self):
        while self.items:
            self.inspect_count += 1
            item = self.items.pop(0)
            new_val = self.operation(item)

            if self.div_by_three:
                new_val //= 3
            else:
                new_val %= self.master_divisor

            if new_val % self.div_test == 0:
                get_monkey_with_id(self.true).items.append(new_val)
            else:
                get_monkey_with_id(self.false).items.append(new_val)

    def __repr__(self):
        return f"{self.items}"


def get_monkey_with_id(id: int) -> Monkey:
    return next(monkey for monkey in Monkey.monkeys if monkey.id == id)

def first_number(string: str):
    return int(re.findall(r'\d+', string)[0])

def part_1():
    with open(f"../inputs/day_11.txt", "r") as input_file:
        for monkey in input_file.read().split('\n\n'):
            id_str, items_str, operation_str, test_str, true_str, false_str = monkey.split("\n")
            id = first_number(id_str)
            items = [int(item) for item in re.findall(r'\d+', items_str)]
            operation = eval("lambda old: " + operation_str.split(" = ")[1])
            div_test = first_number(test_str)
            true = first_number(true_str)
            false = first_number(false_str)
            Monkey(items, div_test, operation, id, true, false)

    m = Monkey.monkeys
    for r in range(20):
        for monkey in sorted(Monkey.monkeys, key=lambda x: x.id):
            monkey.take_turn()

    score = 1
    for m in sorted(Monkey.monkeys, key=lambda x: x.inspect_count)[-2:]:
        score *= m.inspect_count
    print(score)

def part_2():
    with open(f"../inputs/day_11.txt", "r") as input_file:
        for monkey in input_file.read().split('\n\n'):
            id_str, items_str, operation_str, test_str, true_str, false_str = monkey.split("\n")
            id = first_number(id_str)
            items = [int(item) for item in re.findall(r'\d+', items_str)]
            operation = eval("lambda old: " + operation_str.split(" = ")[1])
            div_test = first_number(test_str)
            true = first_number(true_str)
            false = first_number(false_str)
            Monkey(items, div_test, operation, id, true, false, False)

    Monkey.master_divisor = lcm(*[m.div_test for m in Monkey.monkeys])

    m = Monkey.monkeys
    for r in range(10000):
        for monkey in sorted(Monkey.monkeys, key=lambda x: x.id):
            monkey.take_turn()

    score = 1
    for m in sorted(Monkey.monkeys, key=lambda x: x.inspect_count)[-2:]:
        score *= m.inspect_count
    print(score)


if __name__ == "__main__":
    part_1()
    part_2()
