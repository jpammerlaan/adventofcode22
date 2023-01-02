from queue import PriorityQueue
from collections import defaultdict, deque

from utils.io import read_input_file

valves_input = read_input_file(day='16', output_type='list')


def parse_valves(input_valves, start):
    # do some ugly parsing
    valves = {}
    tunnels = {}
    for valve in input_valves:
        flow_part, connections_part = valve.split(';')
        valve_name = flow_part.split(' ')[1]
        flow = int(flow_part.split('=')[1])
        connected = connections_part.split('to ')[1].split(' ')[1:]
        connected = ' '.join(connected).split(', ')
        valves[valve_name] = flow
        tunnels[valve_name] = {c: 1 for c in connected}
    return reduce_tunnels(valves, tunnels, start)


def reduce_tunnels(valves, tunnels, start):
    # for every valve with 0 flow, remove it from the graph
    to_remove = [v for v, flow in valves.items() if flow == 0 and v != start]
    for v in to_remove:
        # connect every connected node to all other connected nodes:
        # i.e. c > v2 directly with distance c > v + 1 instead of c > v > v2
        for c in tunnels[v]:
            for c2 in tunnels[v]:
                if c != c2:
                    tunnels[c][c2] = tunnels[c][v] + tunnels[v][c2]
                    tunnels[c2][c] = tunnels[c2][v] + tunnels[v][c]

    for v in to_remove:
        # remove all the 0-flow valves from the valves, paths and connected nodes
        del tunnels[v]
        del valves[v]
        for v2 in valves.keys():
            if v2 not in to_remove and v in tunnels[v2].keys():
                del tunnels[v2][v]
    return valves, tunnels


def dijkstra(paths, start):
    dist = {v: float('inf') for v in paths.keys()}
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

def bfs(valves, paths, T, start):
    q = deque([(1, start, 0, [start])])
    # get the shortest path from every node to every other node by doing dijkstra
    spt = {pos: dijkstra(paths, pos) for pos in paths.keys()}
    path_flows = defaultdict(int)
    while q:
        t, pos, flow, opened = q.popleft()

        if pos not in opened and t < T:  # open the current valve if not open
            new_opened = opened.copy()
            new_opened.append(pos)
            new_flow = get_flow(valves, pos, t, T)
            q.append((t+1, pos, flow + new_flow, new_opened))
        else:  # try moving to any possible valve from here
            for valve, dt in spt[pos].items():
                if t + dt < T and valve != start and valve not in opened:
                    q.append((t+dt, valve, flow, opened))

        # store the maximum flow for the current path for later use
        key = '|'.join(sorted(opened))
        path_flows[key] = max(path_flows[key], flow)

    return path_flows


def part_one(input_valves, T=30, start='AA'):
    valves, paths = parse_valves(input_valves, start=start)
    best_flows = bfs(valves, paths, T, start)
    return max(best_flows.values())


def part_two(input_valves, T=26, start='AA'):
    valves, paths = parse_valves(input_valves, start=start)
    best_flows = bfs(valves, paths, T, start)
    best = 0
    # Find the best solutions for a set of valves; then for every solution, check if there's also a solution
    # that doesn't intersect with our used valves
    for my_valves, my_flow in best_flows.items():
        my_valves = set(my_valves.split('|')[1:])
        for elephant_valves, elephant_flow in best_flows.items():
            elephant_valves = set(elephant_valves.split('|')[1:])
            if (not my_valves & elephant_valves) and (new_best := my_flow + elephant_flow) > best:
                    best = new_best
    return best

print(f'Part one: {part_one(valves_input)}')
print(f'Part two: {part_two(valves_input)}')
