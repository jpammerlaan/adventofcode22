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
            'false': false_index,
            'inspections': 0
        })
    return monkeys


def part_one(monkeys, rounds=20, hakuna_matata=True):
    upper_bound = math.prod([monkey['div'] for monkey in monkeys])
    for r in range(rounds):
        for i, monkey in enumerate(monkeys):
            for old in monkey['items']:
                # I absolutely hate eval, but it's a necessary evil here
                new = eval(monkey['fn'])
                if hakuna_matata:  # it means don't worry
                    new = math.floor(new / 3)
                # Ensure our numbers don't get too big
                new = new % upper_bound
                # Find the monkey to throw to
                idx = monkey['true'] if new % monkey['div'] == 0 else monkey['false']
                monkeys[idx]['items'].append(new)

            # Finish the turn by adding up inspections and resetting items
            monkey['inspections'] += len(monkey['items'])
            monkey['items'] = []
    print(math.prod(sorted(monkey['inspections'] for monkey in monkeys)[-2:]))


parsed_monkeys = parse_input(monkeys_input)
part_one(parsed_monkeys, 20)
part_one(parsed_monkeys, 10_000, False)
