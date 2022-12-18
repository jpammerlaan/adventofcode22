import numpy as np

from utils.io import read_input_file

droplet_input = read_input_file(day='18', output_type='list')


def parse_droplet(cubes):
    return set([tuple(map(int, c.split(','))) for c in cubes])


def get_neighbors(point):
    directions = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]
    x, y, z = point
    return set((x + dx, y + dy, z + dz) for dx, dy, dz in directions)


def part_one(droplet):
    droplet = parse_droplet(droplet)

    area = 6 * len(droplet)
    for point in droplet:
        area -= len(droplet.intersection(get_neighbors(point)))

    print(f'Part one: {area}')


def part_two(droplet):
    droplet = parse_droplet(droplet)
    min_edge_coord = min(min(point) for point in droplet) - 1
    max_edge_coord = max(max(point) for point in droplet) + 1
    # do a simple BFS to check how many outside borders there are
    # create a bounding box around the droplet, start at its corner and move toward the other corners
    edge = [(min_edge_coord, min_edge_coord, min_edge_coord)]
    outside = set(edge)
    area = 0
    while edge:
        point = edge.pop()
        for neighbor in get_neighbors(point).difference(outside):
            # if we go outside our bounding box, stop there
            if any(c < min_edge_coord for c in point) or any(c > max_edge_coord for c in point):
                continue
            if neighbor in droplet:
                area += 1
            else:
                outside.add(neighbor)
                edge.append(neighbor)

    print(f'Part two: {area}')


part_one(droplet_input)
part_two(droplet_input)
