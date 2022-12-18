from utils.io import read_input_file

rocks_input = read_input_file(day='17', output_type='string').split('\n\n')
jet_pattern = rocks_input.pop(0)


def parse_rocks(input_rocks):
    rocks = []
    for input_rock in input_rocks:
        rock = list()
        for y, row in enumerate(reversed(input_rock.split('\n'))):
            for x, c in enumerate(row):
                if c == '#':
                    rock.append((x, y))
        rocks.append(rock)
    return rocks, len(rocks)


def parse_jet_pattern(pattern):
    return list(map(lambda c: -1 if c == '<' else 1, pattern)), len(pattern)


def init_chamber():
    chamber = [(x, 0) for x in range(7)]
    y_max = 0
    return set(chamber), y_max


def print_chamber(chamber):
    x_max, y_max = max(x for x, y in chamber), max(y for x, y in chamber)
    for y in reversed(range(y_max + 3)):
        for x in range(x_max + 1):
            if (x, y) in chamber:
                print('#', end='')
            else:
                print(' ', end='')
        print('')


def tetris(rocks, jet, R, J, N):
    chamber, y_max = init_chamber()
    seen = {}
    i, j = 0, 0
    cycle_found = False

    while i < N:
        # keep track of the current state: if this state has been seen before, we can use it to detect cycles
        if not cycle_found:
            # Hashing state like this is stolen from another submission, couldn't figure out how to do this effectively.
            state = (i % R, j % J, '|'.join(f'{x},{y - y_max + 10}' for x, y in chamber if y > y_max - 10))
            if state in seen:
                prev_i, prev_y_max = seen[state]
                cycle_found = True
                cycle_length = i - prev_i
                num_cycles_fast_forwarded = (N - i) // cycle_length
                old_i, old_y_max = i, y_max

                i += cycle_length * num_cycles_fast_forwarded
                dy = (y_max - prev_y_max) * num_cycles_fast_forwarded
                y_max += dy
                chamber = set((x, y + dy) for x, y in chamber)
                print(f'Fast forwarding from {old_i} to {i}, increasing y_max by {y_max - old_y_max}')
                print(i, j, chamber, y_max)
            else:
                seen[state] = (i, y_max)
        rock = [(x + 2, y + y_max + 4) for x, y in rocks[i % R]]  # start at x = 2, y_max + 3
        while True:
            # move sideways
            dx = jet[j % J]
            new_rock = [(x + dx, y) for x, y in rock]
            # Only move sideways if we don't go out of bounds or hit another rock
            x_min, x_max = min(x for x, y in new_rock), max(x for x, y in new_rock)
            if x_min >= 0 and x_max < 7 and not any(r in chamber for r in new_rock):
                rock = new_rock
            j += 1
            # move down
            new_rock = [(x, y - 1) for x, y in rock]
            if not any(r in chamber for r in new_rock):  # check if we can move down
                rock = new_rock
            else:  # otherwise, add rock to floor
                for r in rock:
                    chamber.add(r)
                y_max = max(y_max, max(y for x, y in rock))
                break
        i += 1
    print(y_max)


def part_one(rocks, jet, R, J):
    print('Part one: ')
    tetris(rocks, jet, R, J, 2022)


def part_two(rocks, jet, R, J):
    print('Part two: ')
    tetris(rocks, jet, R, J, 1_000_000_000_000)


parsed_rocks, R = parse_rocks(input_rocks=rocks_input)
parsed_jet_pattern, J = parse_jet_pattern(jet_pattern)
# print(parsed_jet_pattern)
# Part one
part_one(rocks=parsed_rocks, jet=parsed_jet_pattern, R=R, J=J)
# Part two
part_two(rocks=parsed_rocks, jet=parsed_jet_pattern, R=R, J=J)
