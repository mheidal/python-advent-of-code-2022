import re
from typing import Tuple, Set, List
import tqdm


Point = Tuple[int, int]  # x,y coords
Range = Tuple[int, int]  # start, end coords in one dimension


def manhattan(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def generate_manhattan_coverage(sensor: Point, beacon: Point) -> Set[Point]:
    coverage = set()
    manhattan_distance = manhattan(sensor, beacon)
    for y in range(-2 * manhattan_distance + sensor[1], 2 * manhattan_distance + sensor[1]):
        for x in range(-2 * manhattan_distance + sensor[0], 2 * manhattan_distance + sensor[0]):
            if manhattan(sensor, (x, y)) <= manhattan_distance:
                coverage.add((x, y))
    return coverage


def intersect(a: Range, b: Range):
    return not (a[1] < b[0] or a[0] > b[1])


def combine_ranges(ranges: List[Range]):
    new_ranges = []
    r_0 = ranges.pop(0)
    while len(ranges) > 1:
        r_1 = ranges.pop(0)
        was_consumed: bool = False
        while intersect(r_0, r_1):
            r_0 = (min(r_0[0], r_1[0]), max(r_0[1], r_1[1]))
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
            sensor = (sensor_x, sensor_y)
            beacon = (beacon_x, beacon_y)
            sensor_beacons.add((sensor, beacon))
            beacons.add(beacon)

    if (-2, 15) in beacons:
        row = 10
    else:
        row = 2000000
    ranges: List[Range] = []
    for sensor, beacon in sensor_beacons:
        if (m_dist := manhattan(sensor, beacon)) >= (dist_to_row := abs(row-sensor[1])):
            flex_along_row = abs(m_dist - dist_to_row)
            cov_along_row = (sensor[0] - flex_along_row, sensor[0] + flex_along_row)
            print(f"Sensor is at {sensor}\n\tmanhattan reach of {m_dist}\n\tdistance to row of {dist_to_row}\n\tcoverage along row of {flex_along_row}\n\trange is {cov_along_row}, length {cov_along_row[1]-cov_along_row[0]+1}")
            ranges.append(cov_along_row)
            ranges = sorted(ranges, key=lambda range_: range_[0])

    ranges = combine_ranges(ranges)
    print(ranges)

    count = 0
    for r in ranges:
        count += r[1] + 1 - r[0]
    count -= len([beacon for beacon in beacons if beacon[1] == row])
    print(count)




def part_2():
    with open(f"../inputs/day_15.txt", "r") as input_file:
        for line in input_file:
            sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall("-?\d+", line))
            sensor = (sensor_x, sensor_y)
            beacon = (beacon_x, beacon_y)
            # plug each of these lines into Desmos graphing calculator
            # solve via visual inspection
            # real solution (todo): find the boundary lines of each manhattan box (which are squares rotated 45 deg)
            # there should be two pairs of lines; each pair is notable because the two elements of the pair are sqrt(2)/2 apart
            # point is at the intersection of the bottom two of those plus one in y direction
            print(rf"abs(x-{sensor_x}) + abs(y-{sensor_y}) < {manhattan(sensor, beacon)}")

if __name__ == "__main__":
    part_1()
    part_2()
