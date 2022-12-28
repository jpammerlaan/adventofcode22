from utils.io import read_input_file

snafu_input = read_input_file(day='25', output_type='list')


SNAFU_TO_DECIMAL = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}
DECIMAL_TO_SNAFU = {v: k for k, v in SNAFU_TO_DECIMAL.items()}

def decode(s):
    d = []
    S = len(s)
    for i, x in enumerate(s):
        d.append(SNAFU_TO_DECIMAL[x] * 5 ** (S-i-1))
    return sum(d)

def encode(d):
    # guess upper bound
    p = 1
    while 2 * (5 ** p) + (2 * 5 ** (p - 1)) < d:
        p += 1
    s = []
    # work your way down, correcting for overshooting in later digits
    for i in range(p, -1, -1):
        j = -2
        while j < 2:
            # correct for whatever you can subtract later
            f = sum(2 * 5 ** (i2 - 1) for i2 in range(i, 0, -1))
            if d - ((j + 1) * 5 ** i) + f < 0:
               break
            j += 1
        d -= j * 5 ** i
        s.append(j)
    return ''.join(DECIMAL_TO_SNAFU[s] for s in s)


def part_one(snafu):
    decimal = map(decode, snafu)
    return encode(sum(decimal))


print(f'Part one: {part_one(snafu_input)}')
