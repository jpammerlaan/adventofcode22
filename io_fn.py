import os


def read_input_file(day, output_type='string'):
    with open(os.path.join('aoc_2022/{}/{}.in'.format(day, day)), 'r') as f:
        input_str = f.read()
    if output_type == 'string':

        input_content = input_str[:-1]  # drop \n
    elif output_type == 'list':
        input_content = input_str.split('\n')[:-1]  # drop empty last line
    else:
        raise ValueError('Unknown output_type {}. Expected string or list.'.format(output_type))
    return input_content


def print_binary_grid(grid, target_val=1):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print('#' if grid[i][j] == target_val else ' ', end='')
        print('')