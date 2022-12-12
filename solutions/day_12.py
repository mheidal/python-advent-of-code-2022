from typing import List, Callable, Tuple


class Node:
    nodes = []
    max_height: int = None
    max_width: int = None

    def __init__(self, id: Tuple[int, int], height: int, is_start: bool, is_end: bool):
        self.id = id
        self.height = height
        self.is_start = is_start
        self.is_end = is_end
        self.neighbors = []
        self.tentative_distance = 0 if is_start else 1_000_000
        self.visited = False
        Node.nodes.append(self)

    def initialize_edges(self, lo_to_hi: bool):
        coords = []
        i, j = self.id
        if not i == 0:
            coords.append((i - 1, j))
        if not i + 1 == Node.max_height:
            coords.append((i + 1, j))
        if not j == 0:
            coords.append((i, j - 1))
        if not j + 1 == Node.max_width:
            coords.append((i, j + 1))
        for coord in coords:
            other = next(node for node in Node.nodes if node.id == coord)
            if lo_to_hi:
                if other.height - self.height <= 1:
                    self.neighbors.append(other)
            else:
                if self.height - other.height <= 1:
                    self.neighbors.append(other)

    def __repr__(self):
        return f"{self.id}, {self.tentative_distance}"


def clean_nodes():
    Node.nodes = []


def dijkstra(targets: List[Node], all_nodes: List[Node]):
    while not any([t.visited for t in targets]) and [
        n for n in all_nodes if not n.visited
    ]:
        current_node = min(
            [n for n in all_nodes if not n.visited], key=lambda x: x.tentative_distance
        )
        for neighbor in current_node.neighbors:
            neighbor.tentative_distance = min(
                neighbor.tentative_distance, current_node.tentative_distance + 1
            )
        current_node.visited = True


def do_search(
    lo_to_hi: bool,
    determine_start: Callable[[str], bool],
    determine_target: Callable[[str], bool],
) -> Node:
    with open(f"../inputs/day_12.txt", "r") as input_file:
        lines = input_file.readlines()
        Node.max_height = len(lines)
        for i, line in enumerate(lines):
            line = line.strip()
            if not Node.max_width:
                Node.max_width = len(line)
            for j, ch in enumerate(line):
                if ch == "S":
                    h = ord("a")
                elif ch == "E":
                    h = ord("z")
                else:
                    h = ord(ch)
                Node((i, j), h, determine_start(ch), determine_target(ch))
    for node in Node.nodes:
        node.initialize_edges(lo_to_hi)
    start = next(node for node in Node.nodes if node.is_start)
    targets = [node for node in Node.nodes if node.is_end]
    dijkstra(targets, Node.nodes)
    return next(n for n in Node.nodes if n.is_end and n.visited)


def part_1():
    target = do_search(
        True,
        lambda x: x == "S",
        lambda x: x == "E",
    )
    print(target.tentative_distance)


def part_2():
    target = do_search(
        False,
        lambda x: x == "E",
        lambda x: x == "S" or x == "a",
    )
    print(target.tentative_distance)


if __name__ == "__main__":
    part_1()
    clean_nodes()
    part_2()
