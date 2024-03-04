"""
Compare the performance of different implementations of the set data structure.
Simple binary tree vs red-black tree.
"""

from time import time
from random import random, randint, choice
from math import log10
import sys
import os

# ugly hack to allow importing from parent directory, since in 50 years python still doesn't have a proper import system outside of modules
# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, "Tree"))

from MultiRedBlackTree import MultiRedBlackTree
from MultiUnbalancedTree import MultiUnbalancedTree


def measure_sequence_of_ops(tree, ops):
    """
    Measures the time it takes to perform a sequence of operations on the tree.
    Parameters:
        tree_implementation: The tree implementation to use.
        ops: Sequence of operations to perform on the tree.
            Each operation is a tuple of the form (operation, value).
            operation is either "add", "remove" or "contains".
            value is the value to add or remove.
    Returns:
        The time it took to perform all operations.
    """
    start_time = time()
    for op, value in ops:
        if op == "add":
            tree.add(value)
        elif op == "remove":
            tree.remove(value)
        elif op == "contains":
            tree.contains(value)
        else:
            raise ValueError(f"Unknown operation {op}")

    return time() - start_time


def generate_op_random_sequence(n, min_val, max_val, add_prob, remove_prob):
    """
    Generates a sequence of operations to perform on a tree.

    It generates n operations, where each operation is either an add, remove or contains, with the given probabilities.
    The probabilty of generating a contains operation is 1 - add_prob - remove_prob.

    The function ensures that the sequence of operations is valid, i.e. if a remove is generated, the value is in the tree.
    Parameters:
        n: The number of operations to generate.
        min_val: The minimum value to use.
        max_val: The maximum value to use.
        add_prob: The probability of generating an add operation.
        remove_prob: The probability of generating a remove operation.
    """
    assert add_prob + remove_prob <= 1

    values_in_tree = set()

    def generate_op():
        nonlocal values_in_tree

        if len(values_in_tree) == 0:
            # If the tree is empty, we can only add
            return "add", randint(min_val, max_val)

        # Generate a random operation
        op = random()

        if op < add_prob:
            # Add
            value = randint(min_val, max_val)
            values_in_tree.add(value)
            return "add", value

        if op < add_prob + remove_prob:
            return "remove", choice(list(values_in_tree))  # not the most efficient way to do this

        # Contains
        return "contains", randint(min_val, max_val)

    return [generate_op() for _ in range(n)]


def generate_add_sequence(n):
    """
    Generates a sequence of n add operations, with sequential values.
    """
    return [("add", i) for i in range(n)]


import matplotlib.pyplot as plt


def main():
    # Random sequence of operations with fully random values
    # export the plot to a pdf file
    plt.figure()
    plt.xlabel("Number of operations")
    plt.ylabel("Time taken (s)")
    plt.title("Comparison of set implementations")
    plt.xscale("log")

    times_unbalanced = []
    times_red_black = []
    for n in [10**i for i in range(1, 8)]:  # 10, 100, 1000, ...
        print(f"n = {n}")
        ops = generate_op_random_sequence(n, 0, n * n, 0.8, 0.1)

        times_unbalanced.append(
            (
                n,
                measure_sequence_of_ops(MultiUnbalancedTree(), ops),
            )
        )

        times_red_black.append(
            (
                n,
                measure_sequence_of_ops(MultiRedBlackTree(), ops),
            )
        )

    plt.plot(*zip(*times_unbalanced), label="Unbalanced")
    plt.plot(*zip(*times_red_black), label="Red-black")
    plt.legend()

    plt.savefig("random_sequence.pdf")

    # Random sequence of operations with values in a range
    plt.figure()
    plt.xlabel("Number of operations")
    plt.ylabel("Time taken (s)")
    plt.title("Comparison of set implementations")
    plt.xscale("log")

    times_unbalanced = []
    times_red_black = []
    for n in [10**i for i in range(1, 6)]:
        print(f"n = {n}")
        ops = generate_add_sequence(n)

        times_unbalanced.append(
            (
                n,
                measure_sequence_of_ops(MultiUnbalancedTree(), ops),
            )
        )

        times_red_black.append(
            (
                n,
                measure_sequence_of_ops(MultiRedBlackTree(), ops),
            )
        )

    plt.plot(*zip(*times_unbalanced), label="Unbalanced")
    plt.plot(*zip(*times_red_black), label="Red-black")
    plt.legend()

    plt.savefig("increasing_sequence.pdf")


if __name__ == "__main__":
    main()
