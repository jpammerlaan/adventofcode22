from collections import defaultdict
from itertools import cycle

from utils.io import read_input_file

map_input = read_input_file(day='24', output_type='list')

BLIZZARD_DIRECTIONS = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}


def parse_map(expedition_map):
    walls = {}
    blizzards = []
    for y, line in enumerate(expedition_map):
        for x, point in enumerate(line):
            if point == '#':
                walls[(x, y)] = 1
            elif point in BLIZZARD_DIRECTIONS.keys():
                blizzards.append(((x, y), BLIZZARD_DIRECTIONS[point]))

    return walls, blizzards


def get_blizzard_cycles(walls, blizzards):
    blizzard_cycles = []
    for (x, y), (dx, dy) in blizzards:
        blizzard_cycle = [(x, y)]
        while True:
            new_pos = (x + dx, y + dy)
            if new_pos in walls.keys():  # we hit a wall, spawn a new blizard
                # find corresponding wall: travel back until we hit a wall
                while (x, y) not in walls.keys():
                    x, y = x - dx, y - dy
                # move one tile and spawn here
                new_pos = (x + dx, y + dy)
            if new_pos in blizzard_cycle:  # we've come full circle
                break
            blizzard_cycle.append(new_pos)
            x, y = new_pos
        blizzard_cycles.append(blizzard_cycle)
    return blizzard_cycles

def get_next_positions(walls, bounds, blizzard_cycles, i, pos):
    possible = []
    x, y = pos
    current_blizzards = [blizzard[(i + 1) % len(blizzard)] for blizzard in blizzard_cycles]
    for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_pos = (x + dx, y + dy)
        if (next_pos not in current_blizzards
            and next_pos not in walls.keys()
            and bounds[0][0] <= next_pos[0] < bounds[0][1] 
            and bounds[1][0] <= next_pos[1] < bounds[1][1]
        ):
            possible.append((i + 1, next_pos))
    return possible

def bfs(walls, blizzards, start, end, start_tick=0):
    blizzard_cycles = get_blizzard_cycles(walls, blizzards)
    q = [(start_tick, start)]
    x_coords, y_coords = zip(*walls.keys())
    x_min, x_max = min(x_coords), max(x_coords) + 1
    y_min, y_max = min(y_coords), max(y_coords) + 1
    bounds = ((x_min, x_max), (y_min, y_max))
    while True:
        i, pos = q.pop(0)
        if pos == end:
            return i
        possible_moves = get_next_positions(walls, bounds, blizzard_cycles, i, pos)
        q.extend(possible_moves)
        q = list(dict.fromkeys(q))

    	# prune the search space back to 100 if there are more than 200 states to check
        n = 100
        if len(q) > 2 * n:
            q = sorted(q, key=lambda q: 1000 * (abs(end[0] - q[1][0]) + abs(end[1] - q[1][1])) + q[0] - start_tick)
            q = list(q[0:n])


def part_one(walls, blizzards):
    start = (1, 0)
    end = (150, 21)
    num_rounds = bfs(walls, blizzards, start=start, end=end)
    return num_rounds


def part_two(walls, blizzards):
    start = (1, 0)
    end = (150, 21)
    num_rounds = bfs(walls, blizzards, start, end)
    num_rounds = bfs(walls, blizzards, start=end, end=start, start_tick=num_rounds)
    num_rounds = bfs(walls, blizzards, start=start, end=end, start_tick=num_rounds)
    return num_rounds

# parsed_walls, parsed_blizzards = parse_map(map_input)
# print(f'Part one: {part_one(parsed_walls, parsed_blizzards)}')
# print(f'Part two: {part_two(parsed_walls, parsed_blizzards)}')


