from io_fn import read_input_file

lines = read_input_file(day='05', output_type='string')


def read_input(lines):
    drawing, instruction_lines = lines.split('\n\n')

    drawing_lines = drawing.split('\n')
    stacks = [list() for _ in drawing_lines.pop().split()]
    for line in reversed(drawing_lines):
        for i in range(len(stacks)):
            if 4 * i + 1 < len(line) and line[4 * i + 1] != ' ':
                stacks[i].append(line[4 * i + 1])

    instructions = [[int(i) for i in line.split(' ')[1::2]] for line in instruction_lines.split('\n')]
    return stacks, instructions


def part_one(stacks, instructions):
    for qty, src, target in instructions:
        for _ in range(qty):
            stacks[target - 1].append(stacks[src - 1].pop())
    print(''.join(stack[len(stack) - 1] for stack in stacks))


def part_two(stacks, instructions):
    for qty, src, target in instructions:
        temp_stack = []
        for _ in range(qty):
            temp_stack.append(stacks[src - 1].pop())
        for _ in range(qty):
            stacks[target - 1].append(temp_stack.pop())
    print(''.join(stack[len(stack) - 1] for stack in stacks))


stacks, instructions = read_input(lines)
part_one(stacks, instructions)
stacks, instructions = read_input(lines)
part_two(stacks, instructions)
