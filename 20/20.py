from collections import deque

from utils.io import read_input_file

encrypted_input = read_input_file(day='20', output_type='list')


def mix(seq):
    S = len(seq)
    for i in range(S):
        current = [x for x in seq if x[0] == i][0]
        current_pos, current_val = seq.index(current), current[1]
        next_pos = (current_pos + current_val) % (S - 1)
        if next_pos == 0:  # if we want to insert at the start, insert at the end instead to stay consistent
            next_pos = len(seq)
        seq.remove(current)
        seq.insert(next_pos, current)
    return seq


def get_coords(seq):
    # lmao
    return sum([seq[idx][1] for idx in
                [(seq.index([x for x in seq if x[1] == 0][0]) + 1000 * i) % len(seq) for i in range(1, 4)]])


def part_one(encrypted):
    seq = deque((i, int(x)) for i, x in enumerate(encrypted))
    seq = mix(seq)
    print(get_coords(seq))


def part_two(encrypted, decrypt_key=811589153):
    seq = deque((i, int(x) * decrypt_key) for i, x in enumerate(encrypted))
    for _ in range(10):
        seq = mix(seq)
    print(get_coords(seq))


part_one(encrypted_input)
part_two(encrypted_input)
