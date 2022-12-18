import numpy as np

from utils.io import read_input_file

cubes_input = read_input_file(day='18', output_type='list')


def parse_cubes(cubes):
    return np.array([tuple(map(int, c.split(','))) for c in cubes])


def part_one(cubes):
    cubes = parse_cubes(cubes)
    sides = 0
    directions = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]
    for d in directions:
        neighbors = cubes + d
        sides += sum(0 if (cube == neighbors).all(axis=1).any() else 1 for cube in cubes)

    print(f'Part one: {sides}')


def part_two(cubes):
    cubes = parse_cubes(cubes)
    sides = 0

    print('Part two: ')


part_one(cubes_input)
part_two(cubes_input)