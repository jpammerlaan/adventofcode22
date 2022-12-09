import numpy as np
from io_fn import read_input_file

input_list = read_input_file(day='09', output_type='list')
instruction_list = [(line[0], int(line[2:])) for line in input_list]

DIRECTION_MAP = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}


def print_visited(visited, minx=0, miny=0, maxx=6, maxy=5):
    for y in reversed(range(miny, maxy)):
        for x in range(minx, maxx):
            print(' ', end='')
            if (x, y) in visited:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def print_knots(knots, minx=0, miny=0, maxx=6, maxy=5):
    for y in reversed(range(miny, maxy)):
        for x in range(minx, maxx):
            print(' ', end='')
            printed = False
            for i, knot in enumerate(knots):
                if (x, y) == tuple(knot):
                    print(i, end='')
                    printed = True
                    break
            if not printed:
                print('.', end='')
        print('')
    print('\n')


def part_one(instructions):
    head = np.array((0., 0.))
    tail = np.array((0., 0.))
    visited = set()
    for direction, n_steps in instructions:
        step = DIRECTION_MAP[direction]
        for i in range(n_steps):
            head += step
            if np.linalg.norm(head - tail) > np.sqrt(2):
                dx, dy = head - tail
                if abs(dx) > 1 or (abs(dx) == 1 and abs(dy) > 1):
                    tail[0] += np.sign(dx)
                if abs(dy) or (abs(dy) == 1 and abs(dx) > 1):
                    tail[1] += np.sign(dy)
            print_knots([head, tail])
            visited.add(tuple(tail))
    # print_visited(visited)
    print(len(visited))


def part_two(instructions):
    knots = [np.array((0., 0.)) for _ in range(10)]  # init 9 knots on 0,0
    updated_knots = []
    visited = set()
    for direction, n_steps in instructions:
        print(f'{direction}' f'{n_steps}')
        step = DIRECTION_MAP[direction]
        for i in range(n_steps):
            head = knots[0]
            head += step
            for tail in knots[1:]:
                if np.linalg.norm(head - tail) > np.sqrt(2):
                    dx, dy = head - tail
                    if abs(dx) > 1 or (abs(dx) == 1 and abs(dy) > 1):
                        tail[0] += np.sign(dx)
                    if abs(dy) or (abs(dy) == 1 and abs(dx) > 1):
                        tail[1] += np.sign(dy)
                updated_knots.append(head)
                head = tail  # set the current knot to the next head
            visited.add(tuple(head))
            updated_knots.append(head)
            knots = updated_knots
            updated_knots = []
    print(len(visited))


# part_one(instructions=instruction_list)
part_two(instructions=instruction_list)
