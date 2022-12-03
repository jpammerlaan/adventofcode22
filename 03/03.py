from io_fn import read_input_file

lines = read_input_file(day='03', output_type='list')


def get_priority(item):
    return (ord(item) - ord('A') + 27) if item.isupper() else ord(item) - ord('a') + 1


def part_one(rucksacks):
    priority = sum([get_priority(set(r[len(r) // 2:]).intersection(set(r[:len(r) // 2])).pop()) for r in rucksacks])
    print(priority)


def part_two(rucksacks):
    priority = sum([get_priority(set(rucksacks[3 * i]).intersection(set(rucksacks[3 * i + 1]), set(rucksacks[3 * i + 2])).pop()) for i in range(len(rucksacks) // 3)])
    print(priority)


part_one(lines)
part_two(lines)
