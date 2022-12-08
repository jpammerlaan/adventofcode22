import numpy as np
from io_fn import read_input_file

tree_input = read_input_file(day='08', output_type='list')
tree_array = np.array([[int(tree) for tree in trees] for trees in tree_input])


def part_one(trees):
    visible = 0
    for y in range(trees.shape[0]):
        for x in range(trees.shape[1]):
            neighbors = trees[y, (x + 1):], trees[y, :x], trees[(y + 1):, x], trees[:y, x]
            if any(trees[y][x] > [n.max() if n.size else - 1 for n in neighbors]):
                visible += 1
    print(visible)


def part_two(trees):
    score = 0
    for y in range(trees.shape[0]):
        for x in range(trees.shape[1]):
            current_score = 1
            neighbors = trees[y, (x + 1):], np.flip(trees[y, :x], 0), trees[(y + 1):, x], np.flip(trees[:y, x], 0)
            for n in neighbors:
                # Good luck figuring this one out
                current_score *= ((np.argmax(n >= trees[y, x]) + 1) if np.max(n) >= trees[y, x] else n.size) if n.size else 1
            score = max(current_score, score)
    print(score)


part_one(trees=tree_array)
part_two(trees=tree_array)
