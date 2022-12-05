from io_fn import read_input_file

lines = read_input_file(day='04', output_type='list')


def part_one(assignments):
    count = 0
    for pair in assignments:
        a, b = [[int(bound) + i for i, bound in enumerate(assignment.split('-'))] for assignment in pair.split(',')]
        assignment_sets = set(range(*a)), set(range(*b))
        if assignment_sets[0].intersection(assignment_sets[1]) in assignment_sets:
            count += 1
    print(count)


def part_two(assignments):
    count = 0
    for pair in assignments:
        a, b = [[int(bound) + i for i, bound in enumerate(assignment.split('-'))] for assignment in pair.split(',')]
        assignment_sets = set(range(*a)), set(range(*b))
        if len(assignment_sets[0].intersection(assignment_sets[1])) > 0:
            count += 1
    print(count)


part_one(lines)
part_two(lines)
