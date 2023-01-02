from queue import PriorityQueue
from collections import defaultdict, deque

from utils.io import read_input_file

valves_input = read_input_file(day='16', output_type='list')


def parse_valves(input_valves, start):
    valves = {}
    tunnels = {}
    for valve in input_valves:
        flow_part, connections_part = valve.split(';')
        valve_name = flow_part.split(' ')[1]
        flow = int(flow_part.split('=')[1])
        connected = connections_part.split('to ')[1].split(' ')[1:]
        connected = ' '.join(connected).split(', ')
        valves[valve_name] = flow
        tunnels[valve_name] = connected
    return reduce_paths(valves, tunnels, start)


def reduce_paths(valves, tunnels, start):
    paths = {}
    for v, connected in tunnels.items():
        paths[v] = defaultdict(int)
        for c in connected:
            paths[v][c] = 1
    to_remove = [v for v, flow in valves.items() if flow == 0 and v != start]
    for v in to_remove:
        flow = valves[v]
        # for every valve with 0 flow, remove it from the graph
        if flow == 0:
            # connect every connected node to all other connected nodes:
            # i.e. c > v2 directly with distance c > v + 1 instead of c > v > v2
            for c in paths[v]:
                for c2 in paths[v]:
                    if c != c2:
                        paths[c][c2] = paths[c][v] + paths[v][c2]
                        paths[c2][c] = paths[c2][v] + paths[v][c]

    for v in to_remove:
        # remove all the 0-flow valves from the valves, paths and connected nodes
        del paths[v]
        del valves[v]
        for v2 in valves.keys():
            if v2 not in to_remove and v in paths[v2].keys():
                del paths[v2][v]
    return valves, paths

def dijkstra(paths, start):
    dist = {v:float('inf') for v in paths.keys()}
    dist[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))
    visited = [start]

    while not pq.empty():
        (_, v) = pq.get()
        visited.append(v)

        for v2, d in paths[v].items():
            if v2 not in visited:
                new_cost = dist[v] + d
                if new_cost < dist[v2]:
                    pq.put((new_cost, v2))
                    dist[v2] = new_cost
    del dist[start]
    return dist


def get_flow(valves, v, t, T):
    return (T - t) * valves[v]

def bfs(valves, paths, T, start, print_best=False):
    max_flow = 0
    q = deque([(1, start, 0, [start], start)])
    # get the shortest path from every node to every other node by doing dijkstra
    dst = {pos: dijkstra(paths, pos) for pos in paths.keys()}
    best_flows = defaultdict(int)
    while q:
        t, pos, flow, opened, path = q.popleft()

        # open the current valve if not open
        if pos not in opened and t < T:
            new_opened = opened.copy()
            new_opened.append(pos)
            new_flow = get_flow(valves, pos, t, T)
            q.append((t+1, pos, flow + new_flow, new_opened, path))

        else:
            # try moving to any possible valve from here
            for valve, dt in dst[pos].items():
                if t + dt < T and valve != start and valve not in opened:
                    q.append((t+dt, valve, flow, opened, path + f' > {valve}'))


        # store the path in best_paths
        key = '|'.join(sorted(opened))
        best_flows[key] = max(best_flows[key], flow)

        # print stuff
        if t == T and flow > max_flow and print_best:
            max_flow = flow
            print(f'New best found at t={t}: open {",".join(opened)} and get total flow {flow}')
            print(f'Took path {path} to get here.\n')

    return best_flows


def part_one(input_valves, T=30, start='AA'):
    valves, paths = parse_valves(input_valves, start=start)
    best_flows = bfs(valves, paths, T, start, print_best=True)
    return max(best_flows.values())


def part_two(input_valves, T=26, start='AA'):
    valves, paths = parse_valves(input_valves, start=start)
    best_flows = bfs(valves, paths, T, start, print_best=True)
    valves_set = set(valves.keys())
    r1 = 'AA|CD|DT|KL|KW|YS'
    r2 = 'AA|DI|DY|OI|OU|RH|TO'
    print(best_flows[r1])
    print(best_flows[r2])
    best, me, elephant = 0, [], []
    for my_valves, my_flow in best_flows.items():
        # Find the best solutions for a set of valves; then for every solution, check if there's also a solution
        # that doesn't intersect with our used valves
        my_valves = set(my_valves.split('|')[1:])
        for elephant_valves, elephant_flow in best_flows.items():
            elephant_valves = set(elephant_valves.split('|')[1:])
            if (not my_valves & elephant_valves) and (new_best := my_flow + elephant_flow) > best:
                    best = new_best
                    me = my_valves
                    elephant = elephant_valves
                    print(f'New best found: {new_best}.')
                    print(f'I open valves {me}, releasing {my_flow} pressure.')
                    print(f'The elephant opens {elephant}, releasing {elephant_flow} pressure.')


print(f'Part one: {part_one(valves_input)}')
part_two(valves_input)
