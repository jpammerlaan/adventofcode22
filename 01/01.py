from io_fn import read_input_file

lines = read_input_file(day='01', output_type='list')


def part_one(elf_calories):
    elves, elf = [], []
    for line in lines:
        if line == '':
            elves.append(elf)
            elf = []
        else:
            elf.append(int(line))

    totals = [sum(elf) for elf in elves]
    sorted_totals = sorted(totals, reverse=True)
    print(f'Part one: {sorted_totals[0]}')
    return sorted_totals


def part_two(sorted_totals):
    print(sum(sorted_totals[0:3]))


sorted_elf_totals = part_one(lines)
part_two(sorted_elf_totals)
