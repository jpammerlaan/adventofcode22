from collections import deque, Counter

from utils.io import read_input_file

map_input = read_input_file(day='23', output_type='list')


def parse_map(elves_map):
    elves = {}
    i = 0
    y_max = len(elves_map)
    for y, line in enumerate(elves_map):
        for x, point in enumerate(line):
            if point == '#':
                elves[(x, y_max - y)] = i
                i += 1
    return elves


def get_options():
    options = [
        [(0, 1), (-1, 1), (1, 1)],     # north
        [(0, -1), (-1, -1), (1, -1)],  # south
        [(-1, 0), (-1, 1), (-1, -1)],  # west
        [(1, 0), (1, 1), (1, -1)],     # east
    ]

    return deque(options)


def propose(elves, pos, options):
    x, y = pos
    # check if there are any adjacent elves; if not, don't move
    adjacent = [(x + dx, y + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]
    adjacent.remove(pos)
    if all(adj not in elves for adj in adjacent):
        return pos, False
    # propose each direction
    for proposal in options:
        # if no elves are in or next to proposal squares, move there
        if all((x + dx, y + dy) not in elves for dx, dy in proposal):
            dx, dy = proposal[0]
            return (x + dx, y + dy), True
    # if no proposal was possible, return the old position
    return pos, True


def print_map(elves):
    coords = elves.keys()
    x_coords, y_coords = zip(*coords)
    x_min, x_max = min(x_coords) - 1, max(x_coords) + 2
    y_min, y_max = min(y_coords) - 2, max(y_coords) + 1
    for y in range(y_max, y_min, - 1):
        for x in range(x_min, x_max):
            if (x, y) in coords:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def run(elves, n_rounds):
    options = get_options()
    print_map(elves)
    for i in range(int(n_rounds)):  # run a round
        # first half, propose new positions:
        moves_needed = False
        proposals = {}
        for pos, elf in elves.items():
            proposal, needs_to_move = propose(elves, pos, options)
            moves_needed = max(needs_to_move, moves_needed)
            proposals[elf] = (pos, proposal)

        if not moves_needed:
            print(f'Nobody needs to move in round {i}, done.')
            return elves, i + 1

        # second half, move if no other elf tries to move here:
        new_elves = {}
        counter = Counter([proposal for _, proposal in proposals.values()])
        for elf, (pos, proposal) in proposals.items():
            # only move elf if they are the only elf proposing to move here
            if counter[proposal] == 1:
                new_elves[proposal] = elf
            else:
                new_elves[pos] = elf

        # Move all the elves
        elves = new_elves
        if i % 100 == 0:
            print(i)
        # Rotate the proposal options so we check other directions first
        options.rotate(-1)
    return elves, i


def get_empty_squares(elves):
    coords = elves.keys()
    x_coords, y_coords = zip(*coords)
    x_min, x_max = min(x_coords), max(x_coords) + 1 
    y_min, y_max = min(y_coords), max(y_coords) + 1
    return (x_max - x_min) * (y_max - y_min) - len(elves)


def part_one(elves):
    elves, _ = run(elves, n_rounds=10)
    print_map(elves)
    return get_empty_squares(elves)


def part_two(elves):
    elves, round = run(elves, n_rounds=1e8)  # just run an arbitrarily large number of rounds
    print_map(elves)
    return round


parsed_elves = parse_map(map_input)
print(f'Part one: {part_one(parsed_elves)}')
print(f'Part two: {part_two(parsed_elves)}')


