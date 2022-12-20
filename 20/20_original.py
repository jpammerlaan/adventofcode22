from collections import deque

from utils.io import read_input_file

encrypted_input = read_input_file(day='20', output_type='list')


def part_one(encrypted):
    seq = deque((i, int(x)) for i, x in enumerate(encrypted))
    S = len(seq)
    print([s[1] for s in seq])
    for i in range(S):
        current = [x for x in seq if x[0] == i][0]
        print(f'Moving {current[1]}...')
        current_pos, current_val = seq.index(current), current[1]
        next_pos = (current_pos + current_val) % (S - 1)
        if next_pos == 0:
            next_pos = len(seq)
        seq.remove(current)
        seq.insert(next_pos, current)
        print([s[1] for s in seq])
    zero = [x for x in seq if x[1] == 0][0]
    zero_pos = seq.index(zero)
    coord_idx = [(zero_pos + 1000 * i) % S for i in range(1, 4)]
    print(coord_idx)
    coord = [seq[idx][1] for idx in coord_idx]
    print(coord)
    print(sum(coord))
