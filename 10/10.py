import numpy as np
from utils.io import read_input_file

instruction_list = read_input_file(day='10', output_type='list')


def process_cycle(cycle, X, strength, crt):
    crt += '#' if cycle % 40 in (X-1, X, X+1) else '.'
    cycle += 1
    if cycle % 40 == 20:
        strength += X * cycle

    return cycle, strength, crt

def run(instructions):
    cycle, strength = 0, 0
    X = 1
    crt = ''
    for instruction in instructions:
        cycle, strength, crt = process_cycle(cycle, X, strength, crt)
        if instruction != 'noop':
            cycle, strength, crt = process_cycle(cycle, X, strength, crt)
            X += int(instruction[5:])
    print(f'Part one: {strength}')
    print('Part two:')
    for i in range(1, 7):
        print(crt[(i-1) * 40: i * 40])


run(instructions=instruction_list)
