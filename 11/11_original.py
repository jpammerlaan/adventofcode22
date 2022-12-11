import math
from utils.io import read_input_file

monkeys_input = read_input_file(day='11', output_type='string')


def parse_input(inp):
    monkeys = []
    for monkey_part in inp.split('\n\n'):
        _, starting_items_str, operation_str, test_str, true_str, false_str = monkey_part.split('\n')
        starting_items = [int(item) for item in starting_items_str[starting_items_str.index(':') + 2:].split(', ')]
        operation_str = operation_str[operation_str.index('=') + 2:]
        division_value = int(test_str.split(' ').pop())
        true_index = int(true_str.split(' ').pop())
        false_index = int(false_str.split(' ').pop())
        monkeys.append({
            'items': starting_items,
            'fn': operation_str,
            'div': division_value,
            'true': true_index,
            'false': false_index
        })
    return monkeys


def part_one(monkeys, rounds=20):
    monkey_range = range(len(monkeys))
    inspections = [0 for _ in monkey_range]
    for r in range(rounds):
        for i in monkey_range:
            monkey = monkeys[i]
            for old in monkey['items']:
                new = eval(monkey['fn'])  # sorry
                new = math.floor(new / 3)
                if new % monkey['div'] == 0:
                    monkeys[monkey['true']]['items'].append(new)
                else:
                    monkeys[monkey['false']]['items'].append(new)
                inspections[i] += 1
            monkey['items'] = []
        # print(f'Round {r}: {[monkey["items"] for monkey in monkeys]}')
        # print(f'Inspections: {inspections}')
    print(math.prod(sorted(inspections, reverse=True)[0:2]))


parsed_monkeys = parse_input(monkeys_input)
part_one(parsed_monkeys, 20)
