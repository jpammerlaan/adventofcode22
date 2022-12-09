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


def get_tail(head, tail):
    if np.linalg.norm(head - tail) > np.sqrt(2):
        dx, dy = head - tail
        if abs(dx) > 1 or (abs(dx) == 1 and abs(dy) > 1):
            tail[0] += np.sign(dx)
        if abs(dy) or (abs(dy) == 1 and abs(dx) > 1):
            tail[1] += np.sign(dy)
    return tail


def part_one(instructions, n_knots):
    knots = [np.array((0., 0.)) for _ in range(n_knots + 1)]  # init 9 knots on 0,0
    visited = set()
    for direction, n_steps in instructions:
        step = DIRECTION_MAP[direction]
        for i in range(n_steps):
            knots[0] += step
            for k, tail in enumerate(knots[1:]):
                knots[k + 1] = get_tail(knots[k], knots[k + 1])
            visited.add(tuple(knots[n_knots]))
    print(len(visited))


part_one(instructions=instruction_list, n_knots=1)
part_one(instructions=instruction_list, n_knots=9)
