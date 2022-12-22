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
                parsed_board[(x + y * 1j)] = c

    # parse path
    path_lengths = map(int, re.split('[RL]', path))
    path_turns = [c for c in path if c in 'RL']
    parsed_path = list(zip(path_lengths, path_turns))

    return parsed_board, parsed_path


def get_start(board, j=0 * 1j):
    x = min(key.real for key in board.keys() if key.imag == j)
    return x + j


def wrap(pos, d, board):
    if d.real > 0:
        return min(key.real for key in board.keys() if key.imag == pos.imag) + pos.imag
    elif d.real < 0:
        return max(key.real for key in board.keys() if key.imag == pos.imag) + pos.imag
    elif d.imag > 0:
        return pos.real + min(key.imag for key in board.keys() if key.real == pos.real)
    elif d.imag < 0:
        return pos.real + max(key.imag for key in board.keys() if key.real == pos.real)
    else:
        return ValueError(f'Incorrect direction {d} specified!')


def get_next_pos(pos, d, board):
    next_pos = pos + d
    if next_pos not in board:
        print('Wrapping around')
        next_pos = wrap(pos, d, board)
    if board[next_pos] == 2:  # run into wall
        print(f'Running into wall at {next_pos}. Returning {pos}.')
        return pos
    return next_pos


def part_one(board):
    board, path = parse_board(board)
    pos = get_start(board)
    d = 1 + 0j
    while path:
        max_steps, turn = path.pop(0)
        print(f'Taking {max_steps} steps, then turning {turn}')
        steps = 0
        while steps < max_steps:
            next_pos = get_next_pos(pos, d, board)
            if next_pos == pos:
                break
            pos = next_pos
            print(f'Moving to {pos}.')

        d = d * 1j if turn == 'R' else d * -1j


part_one(board_input)
