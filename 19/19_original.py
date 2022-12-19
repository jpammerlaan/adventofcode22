import math

import parse

from utils.io import read_input_file

blueprints_input = read_input_file(day='19', output_type='list')


def parse_blueprints(blueprints_input):
    p = parse.compile('Blueprint {i:d}: Each ore robot costs {ore_ore:d} ore. '
                      'Each clay robot costs {ore_clay:d} ore. '
                      'Each obsidian robot costs {ore_obs:d} ore and {clay_obs:d} clay. '
                      'Each geode robot costs {ore_geode:d} ore and {obs_geode:d} obsidian.')
    parsed_blueprints = []
    for blueprint in blueprints_input:
        r = p.parse(blueprint)
        parsed_blueprints.append({
            'identifier': r['i'],
            'ore': (r['ore_ore'], 0, 0, 0),
            'clay': (r['ore_clay'], 0, 0, 0),
            'obs': (r['ore_obs'], r['clay_obs'], 0, 0),
            'geode': (r['ore_geode'], 0, r['obs_geode'], 0)
        })
    return parsed_blueprints


def quality_heuristic(state):
    # As the famous saying goes:
    # 1 geode in the hand is worth 1000 in the bush
    t, (bots, mats, mined) = state
    return 1000*mined[3] + 100*mined[2] + 10*mined[1] + mined[0]


def bfs(reqs, bots, T, N=30_000):
    q = list()
    q.append((0, (bots, (0, 0, 0, 0), (0, 0, 0, 0))))
    score = 0
    d = 0
    while q:
        t, (bots, mats, mined) = q.pop(0)

        if t > d:
            # Prune the search space
            q.sort(key=quality_heuristic, reverse=True)
            q = q[:N]
            d = t

        if t == T:
            score = max(score, mined[3])
            continue

        # Mine ore with the bots
        mats_after_mining = tuple([mats[i] + bots[i] for i in range(4)])
        new_mined = tuple([mined[i] + bots[i] for i in range(4)])

        # Do nothing
        q.append((t + 1, (bots, mats_after_mining, new_mined)))

        for i in range(4):
            bot_cost = reqs[i]

            # Check if we have enough materials to build a robot
            if all([mats[j] >= bot_cost[j] for j in range(4)]):
                new_bots = tuple(bot + 1 if b == i else bot for b, bot in enumerate(bots))

                new_mats = tuple([mats_after_mining[j] - bot_cost[j] for j in range(4)])
                q.append((t + 1, (new_bots, new_mats, new_mined)))
    return score


def part_one(blueprints):
    blueprints = parse_blueprints(blueprints)
    qualities = {}
    for blueprint in blueprints:
        bots = tuple([1, 0, 0, 0])
        reqs = (blueprint['ore'], blueprint['clay'], blueprint['obs'], blueprint['geode'])
        result = bfs(reqs, bots, T=24, N=500)
        print(f'Mined {result} geodes with blueprint {blueprint["identifier"]}, for a score of {result * blueprint["identifier"]}')
        qualities[blueprint['identifier']] = result * blueprint['identifier']
    print(sum(qualities.values()))


def part_two(blueprints):
    blueprints = parse_blueprints(blueprints)[0:3]
    qualities = {}
    for blueprint in blueprints:
        bots = tuple([1, 0, 0, 0])
        reqs = (blueprint['ore'], blueprint['clay'], blueprint['obs'], blueprint['geode'])
        result = bfs(reqs, bots, T=32, N=10_000)
        print(f'Mined {result} geodes with blueprint {blueprint["identifier"]}, for a score of {result}')
        qualities[blueprint['identifier']] = result
    print(math.prod(qualities.values()))


part_one(blueprints_input)
part_two(blueprints_input)
