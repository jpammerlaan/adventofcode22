from io_fn import read_input_file

lines = read_input_file(day='02', output_type='list')


def parse_input(lines):
    return [(ord(line[0]) - ord('A'), ord(line[2]) - ord('X')) for line in lines]


def part_one(games):
    rps_map = {
        0: [1, 2, 0],
        1: [0, 1, 2],
        2: [2, 0, 1]
    }

    score = sum([you + 1 + 3 * rps_map[opp][you] for opp, you in games])
    print(score)


def part_two(games):
    rps_map = {
        0: [2, 0, 1],
        1: [0, 1, 2],
        2: [1, 2, 0]
    }

    score = sum([3 * you + 1 + rps_map[opp][you] for opp, you in games])
    print(score)


games = parse_input(lines)
part_one(games)
part_two(games)
