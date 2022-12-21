from decimal import Decimal
import operator

from utils.io import read_input_file

monkeys_input = read_input_file(day='21', output_type='list')


def parse_monkeys(monkeys):
    parsed_monkeys, known = {}, {}
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '/': operator.floordiv,
        '*': operator.mul
    }
    for monkey in monkeys:
        name, needs = monkey.split(': ')
        if len(needs.split(' ')) > 1:
            arg1, op, arg2 = needs.split(' ')
            parsed_monkeys[name] = (arg1, arg2), ops[op]
        else:
            known[name] = int(needs)
    return parsed_monkeys, known


def find(monkeys, known, to_find='root'):
    while to_find not in known:
        to_del = []
        for m, (needs, op) in monkeys.items():
            n1, n2 = needs
            if n1 in known and n2 in known:
                known[m] = op(known[n1], known[n2])
                to_del.append(m)
        for m in to_del:
            del monkeys[m]
    return known[to_find]


def part_one(monkeys):
    parsed_monkeys, known_at_start = parse_monkeys(monkeys)
    print('Part one:')
    print(find(parsed_monkeys, known_at_start))


def part_two(monkeys):
    # From attempting some random numbers, it seems like 'root' is giant, but goes down almost linearly
    # Then around zero it suddenly shoots to a large negative number.
    # So we can iteratively try to find the root (har har) of the function by finding the first negative input, then
    # reducing the step iteratively to narrow the search space.
    parsed_monkeys, known_at_start = parse_monkeys(monkeys)
    inc = 100_000_000_000_000  # some giant number
    start, stop = 0, inc
    step = (stop - start) // 1_000  # divide into 100 steps
    human = None
    while human is None:  # stop only when we've found the correct input
        for i in range(start, stop, step):
            known_at_start['humn'] = i
            parsed_monkeys['root'] = (parsed_monkeys['root'][0], operator.sub)
            root = find(parsed_monkeys.copy(), known_at_start.copy())
            if root == 0:  # done
                human = i
                break
            elif root < 0:
                # narrow the search space: we know the root is in the final step, so we can reduce
                # the increment to 1/100 of the original and again divide into 1_000 steps
                start = i - step
                inc //= 100
                stop = start + inc
                step = (stop - start) // 1_000
                break
    print('Part two:')
    print(human)


part_one(monkeys_input)
part_two(monkeys_input)
