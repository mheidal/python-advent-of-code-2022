import re
from typing import Tuple, Set, List, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Range(NamedTuple):
    start: int
    end: int


class Line(NamedTuple):
    m: float
    b: float


def manhattan(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def ranges_overlap(a: Range, b: Range) -> bool:
    return not (a.end < b.start or a.start > b.end)


def combine_ranges(ranges: List[Range]):
    new_ranges: List[Range] = []
    r_0 = ranges.pop(0)
    while len(ranges) > 1:
        r_1 = ranges.pop(0)
        was_consumed: bool = False
        while ranges_overlap(r_0, r_1):
            r_0 = Range(min(r_0.start, r_1.start), max(r_0.end, r_1.end))
            if ranges:
                r_1 = ranges.pop(0)
            else:
                break
            was_consumed = True
        new_ranges.append(r_0)
        if was_consumed:
            if ranges:
                r_0 = ranges.pop(0)
        else:
            r_0 = r_1
    return new_ranges


def part_1():
    sensor_beacons: Set[Tuple[Point, Point]] = set()
    beacons: Set[Point] = set()
    with open(f"../inputs/day_15.txt", "r") as input_file:
        for line in input_file:
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall("-?\d+", line))
            sensor = Point(sensor_x, sensor_y)
            beacon = Point(beacon_x, beacon_y)
            sensor_beacons.add((sensor, beacon))
            beacons.add(beacon)

    if (-2, 15) in beacons:
        row = 10
    else:
        row = 2000000
    ranges: List[Range] = []
    for sensor, beacon in sensor_beacons:
        if (m_dist := manhattan(sensor, beacon)) >= (
            dist_to_row := abs(row - sensor.y)
        ):
            flex_along_row = abs(m_dist - dist_to_row)
            cov_along_row = Range(sensor.x - flex_along_row, sensor.x + flex_along_row)
            ranges.append(cov_along_row)
            ranges = sorted(ranges, key=lambda r: r.start)

    ranges = combine_ranges(ranges)

    count = 0
    for r in ranges:
        count += r.end + 1 - r.start
    count -= len([beacon for beacon in beacons if beacon.y == row])
    print(count)


def line_intersection(line_1: Line, line_2: Line) -> Point:
    x = (line_1.b - line_2.b) / (line_2.m - line_1.m)
    y = line_1.m * x + line_1.b
    return Point(round(x), round(y))


def part_2():
    lines: Set[Line] = set()
    with open(f"../inputs/day_15.txt", "r") as input_file:
        for line in input_file:
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall("-?\d+", line))
            sensor = Point(sensor_x, sensor_y)
            beacon = Point(beacon_x, beacon_y)
            dist = manhattan(sensor, beacon)
            points: List[Point] = [
                Point(sensor.x + dist, sensor.y),
                Point(sensor.x - dist, sensor.y),
                Point(sensor.x, sensor.y + dist),
                Point(sensor.x, sensor.y - dist),
            ]
            for a, b in [(a, b) for i, a in enumerate(points) for b in points[i + 1 :]]:
                if not a.x == b.x and not a.y == b.y:
                    m = (a.x - b.x) / (a.y - b.y)
                    b = a.y - m * a.x
                    lines.add(Line(m, b))

    line_pairs: Set[Tuple[Line, Line]] = set()

    for line_1 in lines:
        for line_2 in lines:
            if line_1 is not line_2:
                if (
                    line_1.m == line_2.m
                    and abs(line_1.b - line_2.b) == 2
                    and line_1.b != line_2.b
                ):
                    by_b = lambda x: x.b
                    line_pairs.add(
                        (min(line_1, line_2, key=by_b), max(line_1, line_2, key=by_b))
                    )

    pairs: List[Tuple[Line, Line]] = sorted(list(line_pairs), key=lambda x: x[0].b)
    intersection: Point = line_intersection(
        pairs[0][1], pairs[1][0]
    )  # intersection of lower line from each pair
    print(intersection.x * 4_000_000 + intersection.y)


if __name__ == "__main__":
    part_1()
    part_2()
