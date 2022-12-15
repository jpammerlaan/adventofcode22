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
            # print(f'Starting from: ({sx}, {sy}) until: ({ex}, {ey})')
            for x in range(min(sx, ex), max(sx, ex) + 1):
                for y in range(min(sy, ey), max(sy, ey) + 1):
                    sand_map[(x, y)] = 1
            sx, sy = ex, ey
    return sand_map


def print_sand_map(sand_map, to_file=False):
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
    while True:  # keep dropping
        next_pos = get_next_pos(x, y)
        if next_pos[1] >= max_y:  # stop falling after passing last rock
            return sand_map
        if next_pos == (x, y):
            break
        x, y = next_pos
    sand_map[(x, y)] = 2
    return sand_map


def count_dropped_sand(sand_map):
    return sum(1 if sand_map[c] == 2 else 0 for c in sand_map.keys())


def simulate(sand_map, max_y, print_interval=100):
    sand_dropped = count_dropped_sand(sand_map)
    i = 0
    while True:
        new_sand_map = drop_sand(sand_map, max_y=max_y)
        if i % 100 == 0:
            print(i)
        if i % print_interval == 0:
            print_sand_map(sand_map)
        if (new_sand_dropped := count_dropped_sand(new_sand_map)) > sand_dropped:
            sand_dropped = new_sand_dropped
            sand_map = new_sand_map
        else:
            break
        i += 1
    print_sand_map(sand_map)
    print(count_dropped_sand(sand_map))


def part_one(sand_map):
    max_y = max(r[1] for r in sand_map.keys())
    simulate(sand_map, max_y)


def part_two(sand_map):
    max_y = max(r[1] for r in sand_map.keys()) + 2
    for x in range(SAND_START[0] - max_y - 2, SAND_START[0] + max_y + 2):  # make it definitely wide enough
        sand_map[(x, max_y)] = 1
    # print_sand_map(sand_map)
    simulate(sand_map, max_y, print_interval=500)


SAND_START = (500, 0)
sand_map = create_sand_map(rocks)
# print(sand_map)
print_sand_map(sand_map)

# part_one(sand_map)
part_two(sand_map)
