import parse
from utils.io import read_input_file

sensors_input = read_input_file(day='15', output_type='list')


def parse_sensors(sensors):
    p = parse.compile("Sensor at x={xs:d}, y={ys:d}: closest beacon is at x={xb:d}, y={yb:d}")
    parsed_sensors = [((parsed['xs'], parsed['ys']), (parsed['xb'], parsed['yb']),
                       abs(parsed['xs'] - parsed['xb']) + abs(parsed['ys'] - parsed['yb'])  # Manhattan dist between s and b
                       ) for parsed in map(p.parse, sensors)]
    return parsed_sensors


def part_one(sensors, y=10):
    no_beacon_ranges = get_no_beacon_ranges(sensors, y=y)
    merged_ranges = merge_ranges(no_beacon_ranges)
    no_beacon_set = set()
    for start, stop in merged_ranges:
        no_beacon_set = no_beacon_set.union(set(range(start, stop)))
    # Subtract the actual beacons in (x, t_y) at the end
    beacons_at_y = set([b[0] for _, b, _ in sensors if b[1] == y])
    print(len(no_beacon_set.difference(beacons_at_y)))


def get_no_beacon_ranges(sensors, y):
    no_beacon_ranges = list()
    for s, b, r in sensors:
        sx, sy = s
        dx = r - abs(y - sy)
        if dx > 0:
            no_beacon_ranges.append((sx - dx, sx + dx))
    return no_beacon_ranges


def merge_ranges(ranges):
    ranges = sorted(ranges, key=lambda x: x[0])
    merged_ranges = []
    current_range = ranges[0]
    for r in ranges[1:]:
        if r[0] <= current_range[1] or r[0] == current_range[1] + 1:
            # print(f'Merging {current_range} and {r} into {(min(current_range[0], r[0]), max(current_range[1], r[1]))}.')
            current_range = (min(current_range[0], r[0]), max(current_range[1], r[1]))
        else:
            merged_ranges.append(current_range)
            current_range = r
    merged_ranges.append(current_range)
    return merged_ranges


def part_two(sensors):
    for y in range(4_000_000):
        if y % 100_000 == 0:
            print(f'Testing y={y}')
        no_beacon_ranges = get_no_beacon_ranges(sensors, y)
        merged_ranges = merge_ranges(no_beacon_ranges)
        # print(merged_ranges)
        if len(merged_ranges) > 1:
            return 4000000 * (merged_ranges[0][1] + 1) + y


parsed_sensors = parse_sensors(sensors_input)

part_one(parsed_sensors, y=2_000_000)
print(part_two(parsed_sensors))
