import math
from utils.io import read_input_file

input_signals = read_input_file(day='13', output_type='string')


def compare(first, second):
    i = 0
    # Check empty lists first, much easier
    if not (any(c.isnumeric() for c in first)):
        if len(first) < len(second):
            # print(f'{first} is smaller than {second}')
            return True
        else:
            # print(f'{first} is NOT smaller than {second}')
            return False
    while True:
        # print(first[i], second[i])
        # print(i, len(first), len(second))
        # if first[i] == ']':
        #     print(i, len(first), first, i == len(first) - 1)
        if first[i] == ']' and (i == len(first) - 1 or second[i].isnumeric() or second[i] == ',' or second[i] == '['):
            # print(f'{first} is smaller than {second}')
            return True
        if second[i] == ']' and (i == len(second) - 1 or first[i].isnumeric() or first[i] == ',' or first[i] == '['):
            # print(f'{first} is NOT smaller than {second}')
            return False
        if first[i] == second[i]:
            i += 1
            continue
        if first[i] == '[':
            second = second[:i] + '[' + second[i:]
            continue
        if second[i] == '[':
            first = first[:i] + '[' + first[i:]
            continue
        if first[i].isnumeric() and second[i].isnumeric():
            j, k = i, i
            while first[j + 1].isnumeric():
                j += 1
            while second[k + 1].isnumeric():
                k += 1
            if int(first[i:j + 1]) < int(second[i:k + 1]):
                # print(f'{first} is smaller than {second}')
                return True
            else:
                # print(f'{first} is NOT smaller than {second}')
                return False
        if first[i] < second[i]:
            # print(f'{first} is smaller than {second}')
            return True
        # print(f'{first} is NOT smaller than {second}')
        return False


def print_ordered_pairs(ordered_pairs):
    for first, second, ordered in ordered_pairs:
        print(first)
        print(second)
        print(ordered)


def part_one(input_packets):
    pairs = [pair.split('\n') for pair in input_packets.split('\n\n')]
    ordered_pairs = [(first, second, compare(first, second)) for first, second in pairs]
    # print_ordered_pairs(ordered_pairs)
    print(sum(i + 1 for i, info in enumerate(ordered_pairs) if info[2]))


def part_two(packets):
    packets = packets.replace('\n\n', '\n').splitlines()
    divider_packets = ['[[2]]', '[[6]]']
    for packet in divider_packets:
        packets.append(packet)
    # just do a hopelessly slow sort
    sorted_packets = ['[]']
    for x in packets:
        for i, y in enumerate(sorted_packets):
            if compare(x, y):
                sorted_packets.insert(i, x)
                break
        sorted_packets.append(x)
    print(math.prod(sorted_packets.index(packet) for packet in divider_packets))


part_one(input_signals)
part_two(input_signals)
