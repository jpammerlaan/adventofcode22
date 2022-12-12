from utils.io import read_input_file

input_map = read_input_file(day='12', output_type='list')


def parse_input(inp):
    grid = [[ord(x) - ord('a') for x in line] for line in inp]
    start, end = get_grid_idx(grid, -14).pop(), get_grid_idx(grid, -28).pop()
    sx, sy = start
    ex, ey = end
    grid[sy][sx] = 0  # manually set to 0 so shortest path works
    grid[ey][ex] = 26  # manually set to 26 so shortest path works
    return grid, start, end


def get_grid_idx(grid, val):
    idx = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == val:
                idx.append((x, y))
    return idx


def find_neighbors(grid, node, seen, w, h):
    x, y = node
    neighbors = [(max(x - 1, 0), y), (min(x + 1, w - 1), y), (x, max(y - 1, 0)), (x, min(y + 1, h - 1))]
    return [(xn, yn) for xn, yn in neighbors if (xn, yn) not in seen and grid[yn][xn] - grid[y][x] <= 1]


def bfs(grid, start, end):
    h, w = len(grid), len(grid[0])
    shortest_dist = {(x, y): 1e5 for y in range(h) for x in range(w)}
    shortest_dist[start] = 0
    seen = set()

    q = [start]
    while len(q):
        current = q.pop(0)
        if current in seen:
            continue

        neighbors = find_neighbors(grid, current, seen, w, h)
        for n in neighbors:
            dist = shortest_dist[current] + 1
            shortest_dist[n] = min(shortest_dist[n], dist)
            q.append(n)

        seen.add(current)
        if current == end:
            return shortest_dist[current]
    return 1e5


def part_one(grid, start, end):
    print(bfs(grid, start, end))


def part_two(grid, end):
    min_steps = 1e7
    for start in get_grid_idx(grid, 0):
        curr = bfs(grid, start, end)
        min_steps = min(min_steps, curr)
    print(min_steps)


map_grid, S, E = parse_input(input_map)
part_one(map_grid, S, E)
map_grid, _, E = parse_input(input_map)
part_two(map_grid, E)
