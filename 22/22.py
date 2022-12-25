import re
import numpy as np
from collections import defaultdict

from utils.io import read_input_file

board_input = read_input_file(day='22', output_type='list')


def parse_board(board):
    path = board.pop()
    board.pop()

    # parse board
    board_map = {
        ' ': 0,
        '.': 1,
        '#': 2
    }
    parsed_board = defaultdict(int)
    X, Y = max(len(row) for row in board), len(board)
    for y in range(Y):
        for x in range(X):
            if x >= len(board[y]):
                break
            if (c := board_map[board[y][x]]) > 0:
                parsed_board[(x - y * 1j)] = c

    # parse path
    path_lengths = map(int, re.split('[RL]', path))
    path_turns = [c for c in path if c in 'RL']
    path_turns.append('X') # add a fake turn at the end
    parsed_path = list(zip(path_lengths, path_turns))

    return parsed_board, parsed_path


def get_start(board, j=0 * 1j):
    x = min(key.real for key in board.keys() if key.imag == j)
    return x + j


def wrap(pos, d, board):
    if d.real > 0:
        return min(key.real for key in board.keys() if key.imag == pos.imag) + pos.imag * 1j
    elif d.real < 0:
        return max(key.real for key in board.keys() if key.imag == pos.imag) + pos.imag * 1j
    elif d.imag > 0:
        return pos.real + min(key.imag for key in board.keys() if key.real == pos.real) * 1j
    elif d.imag < 0:
        return pos.real + max(key.imag for key in board.keys() if key.real == pos.real) * 1j
    else:
        return ValueError(f'Incorrect direction {d} specified!')


def get_block(pos):
    # hard code this based on the map we drew by hand (very professional)
    x, y = pos.real, -1 * pos.imag
    if x < 50:
        if y < 150:
            return 4
        else:
            return 6
    elif x < 100:
        if y < 50:
            return 1
        elif y < 100:
            return 3
        else:
            return 5
    else:
        return 2


def wrap_3d(pos, d):
    # just hard code this too, sorry about that. This may or may not have taken 2 hours of debugging 
    # because it's Christmas and I can't math good...
    old_block = get_block(pos)
    # Map goes: (old_block, old_direction) -> (new_block, new_direction, pos_translate_fn)
    mapping_dict = {
        (1, (-1 + 0j)): (4, (1 + 0j), lambda p: 0 - (149 + p.imag) * 1j ),
        (1, (0 + 1j)): (6, (1 + 0j), lambda p: 0 - (100 + p.real) * 1j),
        (2, (1 + 0j)): (5, (-1 + 0j), lambda p: 99 - (149 + p.imag) * 1j),
        (2, (0 + 1j)): (6, (0 + 1j), lambda p: (p.real - 100) - 199j),
        (2, (0 - 1j)): (3, (-1 + 0j), lambda p: 99 - (p.real - 50) * 1j),
        (3, (1 + 0j)): (2, (0 + 1j), lambda p: (50 - p.imag) - 49j),
        (3, (-1 + 0j)): (4, (0 - 1j), lambda p: (-50 - p.imag) - 100j),
        (4, (-1 + 0j)): (1, (1 + 0j), lambda p: 50 + (-149 - p.imag) * 1j),
        (4, (0 + 1j)): (3, (1 + 0j), lambda p: 50 - (50 + p.real) * 1j),
        (5, (1 + 0j)): (2, (-1 + 0j), lambda p: 149 - (149 + p.imag) * 1j),
        (5, (0 - 1j)): (6, (-1 + 0j), lambda p: 49 + (-100 - p.real) * 1j),
        (6, (1 + 0j)): (5, (0 + 1j), lambda p: (-100 - p.imag   - 149j)),
        (6, (-1 + 0j)): (1, (0 - 1j), lambda p: (-100 - p.imag) - 0j),
        (6, (0 - 1j)): (2, (0 - 1j), lambda p: 100 + p.real - 0j)
    }
    _, new_d, new_pos_fn = mapping_dict[(old_block, d)]
    return new_pos_fn(pos), new_d


def get_next_pos(pos, d, board, n_dim=2):
    next_pos = pos + d
    new_d = d
    if next_pos not in board:
        if n_dim == 2:
            next_pos = wrap(pos, d, board)
        elif n_dim == 3:
            next_pos, new_d = wrap_3d(pos, d)
    if board[next_pos] == 2:  # run into wall
        new_d = d  # reset the direction to the old direction in case of impossible 3D wrap
        return pos, d
    return next_pos, new_d


def get_facing(d):
    return 2 * (np.angle(np.conj(d)) / np.pi) % 4


def get_final_position(board, n_dim=2):
    board, path = parse_board(board)
    pos = get_start(board)
    d = 1 + 0j
    while path:
        max_steps, turn = path.pop(0)
        steps = 0
        while steps < max_steps:
            next_pos, d = get_next_pos(pos, d, board, n_dim)
            if next_pos == pos:
                break
            pos = next_pos
            steps += 1
        if turn != 'X':  # skip the fake turn at the end
            d = d * -1j if turn == 'R' else d * 1j
    return pos, d


def get_password(p, d):
    f = get_facing(d)
    return int(-1000 * (p.imag - 1) + 4 * (p.real + 1) + f)


def part_one(board):
    final_position, final_direction = get_final_position(board)
    return get_password(final_position, final_direction)


def part_two(board):
    final_position, final_direction = get_final_position(board, n_dim=3)
    return get_password(final_position, final_direction)


print(f'Part one: {part_one(board_input.copy())}')
print(f'Part two: {part_two(board_input.copy())}')
