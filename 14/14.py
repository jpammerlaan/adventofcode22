from collections import defaultdict
from utils.io import read_input_file

rocks = read_input_file(day='14', output_type='list')


def create_sand_map(rock_paths):
    sand_map = defaultdict(int)
    for rock_path in rock_paths:
        sx, sy = None, None
        for stretch in rock_path.split(' -> '):
            ex, ey = map(int, stretch.split(','))
            if sx is None:
                sx, sy = ex, ey
            for x in range(min(sx, ex), max(sx, ex) + 1):
                for y in range(min(sy, ey), max(sy, ey) + 1):
                    sand_map[(x, y)] = 1
            sx, sy = ex, ey
    return sand_map


def print_sand_map(sand_map):
    xrange, yrange = zip(*sand_map.keys())
    xmin, xmax = min(xrange), max(xrange) + 1
    ymin, ymax = 0, max(yrange) + 1
    for y in range(0, ymax):
        for x in range(xmin, xmax):
            if (x, y) == SAND_START:
                print('+', end='')
            elif sand_map[(x, y)] == 0:
                print(' ', end='')
            elif sand_map[(x, y)] == 1:
                print('#', end='')
            elif sand_map[(x, y)] == 2:
                print('o', end='')
            else:
                raise ValueError(f'Unexpected sand map value at ({x}, {y}): {sand_map[(x, y)]}')
        print()


def get_next_pos(x, y):
    for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
        next_pos = (x + dx, y + dy)
        if sand_map[next_pos] == 0:
            return next_pos  # next position is available, we're done
    return x, y


def drop_sand(sand_map, max_y):
    x, y = SAND_START
    while True:  # keep dropping until sand is blocked
        next_pos = get_next_pos(x, y)
        if next_pos[1] >= max_y:  # stop falling after passing last rock
            return sand_map, False
        if next_pos == (x, y):
            break
        x, y = next_pos
    if sand_map[(x, y)] == 2:
        return sand_map, False
    sand_map[(x, y)] = 2
    return sand_map, True


def count_dropped_sand(sand_map):
    return sum(1 if sand_map[c] == 2 else 0 for c in sand_map.keys())


def simulate(sand_map, max_y):
    i = 0
    sand_added = True
    while sand_added:
        sand_map, sand_added = drop_sand(sand_map, max_y=max_y)
        i += 1
    print_sand_map(sand_map)
    print(count_dropped_sand(sand_map))
    return sand_map


def part_one(sand_map):
    max_y = max(r[1] for r in sand_map.keys())
    return simulate(sand_map, max_y)


def part_two(sand_map):
    max_y = max(r[1] for r in sand_map.keys()) + 2
    for x in range(SAND_START[0] - max_y - 2,
                   SAND_START[0] + max_y + 2):  # create the floor, making it wide enough so sand can never fall off it
        sand_map[(x, max_y)] = 1
    simulate(sand_map, max_y)


SAND_START = (500, 0)
sand_map = create_sand_map(rocks)

sand_map = part_one(sand_map)
part_two(sand_map)
