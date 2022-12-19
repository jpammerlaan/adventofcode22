import math

import parse

from utils.io import read_input_file

blueprints_input = read_input_file(day='19', output_type='list')


def parse_blueprints(blueprints_input):
    p = parse.compile('Blueprint {i:d}: Each ore robot costs {ore_ore:d} ore. '
                      'Each clay robot costs {ore_clay:d} ore. '
                      'Each obsidian robot costs {ore_obs:d} ore and {clay_obs:d} clay. '
                      'Each geode robot costs {ore_geode:d} ore and {obs_geode:d} obsidian.')
    parsed_blueprints = {}
    for blueprint in blueprints_input:
        r = p.parse(blueprint)
        parsed_blueprints[r['i']] = {
            'ore': (r['ore_ore'], 0, 0, 0),
            'clay': (r['ore_clay'], 0, 0, 0),
            'obs': (r['ore_obs'], r['clay_obs'], 0, 0),
            'geode': (r['ore_geode'], 0, r['obs_geode'], 0)
        }
    return parsed_blueprints


def quality_guess(state):
    _, (_, _, performance) = state
    return sum(math.pow(10, i) * performance[i] for i in range(len(performance)))


def bfs(reqs, T, N):
    # Create a queue with the time t and the state: our bots, the available mats and our current performance num_mined
    queue = [(0, ((1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))]
    score, max_depth = 0, 0
    while queue:
        t, (bots, mats, num_mined) = queue.pop(0)

        if t > max_depth:
            # Prune the search space by only keeping the N best guesses
            queue.sort(key=quality_guess, reverse=True)
            queue = queue[:N]
            max_depth = t

        if t == T:
            score = max(score, num_mined[3])
            continue

        # mine some ore
        mats_after_mining = tuple([mats[i] + bots[i] for i in range(4)])
        new_mined = tuple([num_mined[i] + bots[i] for i in range(4)])

        # building nothing is always an option
        queue.append((t + 1, (bots, mats_after_mining, new_mined)))

        for i in range(4):
            bot_cost = reqs[i]

            # if we can build a robot, investigate that path
            if all([mats[j] - bot_cost[j] >= 0 for j in range(4)]):
                new_bots = tuple(bot + 1 if b == i else bot for b, bot in enumerate(bots))
                new_mats = tuple([mats_after_mining[j] - bot_cost[j] for j in range(4)])
                queue.append((t + 1, (new_bots, new_mats, new_mined)))
    return score


def part_one(blueprints):
    blueprints = parse_blueprints(blueprints)
    qualities = {}
    for id, blueprint in blueprints.items():
        reqs = (blueprint['ore'], blueprint['clay'], blueprint['obs'], blueprint['geode'])
        result = bfs(reqs, T=24, N=1_000)
        print(f'Mined {result} geodes with blueprint {id}, for a score of {result * id}.')
        qualities[id] = result * id
    print(sum(qualities.values()))


def part_two(blueprints):
    blueprints = {id: blueprint for id, blueprint in parse_blueprints(blueprints).items() if id <= 3}
    qualities = {}
    for id, blueprint in blueprints.items():
        reqs = (blueprint['ore'], blueprint['clay'], blueprint['obs'], blueprint['geode'])
        result = bfs(reqs, T=32, N=5_000)
        print(f'Mined {result} geodes with blueprint {id}, for a score of {result}.')
        qualities[id] = result
    print(math.prod(qualities.values()))


part_one(blueprints_input)
part_two(blueprints_input)
