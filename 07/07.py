from collections import defaultdict
from io_fn import read_input_file

input_commands = read_input_file(day='07', output_type='list')


def get_dirs_with_files(commands):
    dirs = defaultdict(list)
    cwd = []
    for cmd in commands:
        if cmd.startswith('$ cd'):
            d = cmd.split(' ').pop()
            cwd.pop() if d == '..' else cwd.append(d)
        elif cmd.startswith('$ ls') or cmd.startswith('dir'):
            continue
        else:
            size, f = cmd.split(' ')
            # Add file to every directory (in)directly containing it
            for i in range(len(cwd) + 1):
                dirs['/'.join(cwd[:i])].append(int(size))
    return dirs


def part_one(commands):
    dirs = get_dirs_with_files(commands)
    dir_sizes = [sum(files) for d, files in dirs.items()]

    print(sum(size for size in dir_sizes if size <= 100_000))


def part_two(commands):
    dirs = get_dirs_with_files(commands)
    dir_sizes = [sum(files) for d, files in dirs.items()]

    target_size = 70_000_000 - 30_000_000
    to_delete = max(dir_sizes) - target_size
    print(min(size for size in dir_sizes if size >= to_delete))


part_one(commands=input_commands)
part_two(commands=input_commands)
