from io_fn import read_input_file

input_buffer = read_input_file(day='06', output_type='string')


def find_marker(buffer, marker_length):
    for i in range(len(buffer)):
        if len(set(buffer[i:i + marker_length])) == marker_length:
            return i + marker_length


def part_one(buffer):
    print(find_marker(buffer, marker_length=4))


def part_two(buffer):
    print(find_marker(buffer, marker_length=14))


part_one(buffer=input_buffer)
part_two(buffer=input_buffer)
