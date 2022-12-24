from typing import List, Tuple, Dict, Any


class Monkey:
    symbol_to_inv = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*",
        "=": "="
    }

    def __init__(self, name: str, left_name: str, right_name: str, op_symbol: str):
        self.name: str = name
        if op_symbol in "+-*/":  # Monkeys which depend on other monkeys have a reference to their math operation.
            self.operation_symbol = op_symbol
            self.resolved = False
            self.val = None
        else:  # Monkeys which shout their number start resolved and have no ref to a math op.
            self.operation_symbol = None
            self.resolved = True
            self.val = int(op_symbol)

        self.left_name: str = left_name
        self.right_name: str = right_name
        self.left = None
        self.right = None
        self.depth = -1

    def op(self, a, b, inv: bool = False):
        symbol = self.symbol_to_inv[self.operation_symbol] if inv else self.operation_symbol
        if symbol == "+":
            return a + b
        elif symbol == "-":
            return a - b
        elif symbol == "*":
            return a * b
        elif symbol == "/":
            return a / b
        elif symbol == "=":
            return a
        raise ValueError

    def inv_op(self, a, b):
        return self.op(a, b, inv=True)

    def add_children(self, all_monkeys: Dict[str, Any]) -> None:
        """
        Adds references to other monkeys which this monkey depends on.
        :param all_monkeys:
        :return:
        """
        if not self.left_name:
            return
        self.left = all_monkeys[self.left_name]
        self.right = all_monkeys[self.right_name]

    def ready_to_resolve_from_below(self) -> bool:
        """
        Whether the monkey is ready to resolve given the statuses of its children.
        Resolution is assigning a value to the monkey based on its children and operation.
        Monkeys without children start out resolved.
        If the monkey has children and both children are resolved, it's ready to resolve.
        :return: Whether the monkey is ready to resolve.
        """

        if self.left is None:
            return False
        return (
                not self.resolved
                and self.left.resolved
                and self.right.resolved
        )

    def resolve_from_below(self) -> None:
        """
        Assign a val to this monkey based on its operation and the values of the monkeys it depends on.
        If it depends on no monkeys, its operation just returns a number.
        :return:
        """
        self.resolved = True
        self.val = self.op(self.left.val, self.right.val)

    def unresolve(self):
        """Should only be applied to humn."""
        self.resolved = False
        self.val = None

    def assign_depth(self, depth: int):
        """For troubleshooting purposes."""
        self.depth = depth
        if self.left is not None:
            self.left.assign_depth(depth + 1)
            self.right.assign_depth(depth + 1)

    def __repr__(self):
        s = f"{self.name} | val: {self.val}"
        if self.operation_symbol:
            s += f" | op: {self.operation_symbol}"
        return s


def set_up_monkeys() -> Tuple[List[str], Dict[str, Monkey]]:
    """
    Returns a list of monkey names and a dict of Monkey objects arranged in a tree structure.
    Monkeys are assigned children, an operation, and an inverse operation.
    Keys in the dict are monkey names, values are Monkey objects.
    Items in the list are monkey names, sorted by depth, leaves to root.
    :return:
    """
    monkeys = {}
    with open(f"../inputs/day_21.txt", "r") as input_file:
        for line in input_file.readlines():
            name, operation = line.strip().split(": ")
            args = operation.split(' ')
            if len(args) == 1:
                op_symbol = args[0]
                left_name, right_name = None, None
            else:
                left_name, op_symbol, right_name = args
            monkey = Monkey(
                name=name,
                left_name=left_name,
                right_name=right_name,
                op_symbol=op_symbol,
            )
            monkeys[name] = monkey
    for name, monkey in monkeys.items():
        monkey.add_children(monkeys)
    monkeys['root'].assign_depth(0)
    # list of names in descending order of depth allows for resolution of monkey values in order
    names: List[str] = [monkey.name for monkey in sorted(list(monkeys.values()), key=lambda x: x.depth, reverse=True)]
    return names, monkeys


def part_1():
    names, monkeys = set_up_monkeys()
    # resolve all monkeys
    while any(not monkeys[m].resolved for m in names):
        for name in names:
            monkey = monkeys[name]
            if monkey.ready_to_resolve_from_below():
                monkey.resolve_from_below()
    print(monkeys['root'].val)


def part_2():
    names, monkeys = set_up_monkeys()
    # humn is
    monkeys['humn'].val = 1j
    while any(not monkeys[m].resolved for m in names):
        for name in names:
            monkey = monkeys[name]
            if monkey.ready_to_resolve_from_below():
                monkey.resolve_from_below()
    root = monkeys['root']
    unresolved = root.left.val if root.left.val.imag != 0 else root.right.val
    resolved = root.left.val if unresolved == root.right.val else root.right.val
    print((resolved - unresolved.real) / unresolved.imag)
    # monkeys['humn'].unresolve()
    # root = monkeys['root']
    # root.operation_symbol = "="
    # # progressively resolve until all monkeys are resolved except those in the chain from humn to root
    # num_changed = -1
    # while num_changed != 0:
    #     num_changed = 0
    #     for name in names:
    #         monkey = monkeys[name]
    #         if monkey.ready_to_resolve_from_below():
    #             monkey.resolve_from_below()
    #             num_changed += 1
    # parent = root
    # requirement = root.left.val if root.left.resolved else root.right.val
    # while parent.name != "humn":
    #     resolved_child = parent.left if parent.left.resolved else parent.right
    #     new_requirement = parent.inv_op(requirement, resolved_child.val)
    #     req_str = str(requirement)
    #     val_str = str(resolved_child.val)
    #     new_str = str(new_requirement)
    #     max_len = max(len(req_str), len(val_str), len(new_str)) + 2
    #     print(f"Depth {resolved_child.depth}: parent is {parent}\n"
    #           f"{req_str.rjust(max_len, ' ')}  (previous required value)\n"
    #           f"{Monkey.symbol_to_inv[parent.operation_symbol]}{val_str.rjust(max_len - 1, ' ')}  (resolved child)\n"
    #           f"{'-' * max_len}\n"
    #           f"{new_str.rjust(max_len, ' ')} (next required value)\n")
    #     if new_requirement != int(new_requirement):
    #         raise ValueError
    #     requirement = new_requirement
    #     parent = parent.left if resolved_child is parent.right else parent.right
    # print(requirement)


if __name__ == "__main__":
    part_1()
    part_2()
