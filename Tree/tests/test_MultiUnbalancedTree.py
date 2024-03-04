import sys
import os

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)


import pytest
import random
from MultiUnbalancedTree import MultiUnbalancedTree


@pytest.fixture
def empty_tree():
    return MultiUnbalancedTree()


@pytest.fixture
def filled_tree():
    tree = MultiUnbalancedTree()
    for value in [5, 3, 7, 2, 4, 6, 8]:
        tree.add(value)
    return tree


def test_iter1(empty_tree):
    assert list(empty_tree) == []
    empty_tree.add(1)
    assert list(empty_tree) == [1]
    empty_tree.add(2)
    assert list(empty_tree) == [1, 2]
    empty_tree.add(3)
    assert list(empty_tree) == [1, 2, 3]
    empty_tree.remove(2)
    assert list(empty_tree) == [1, 3]
    empty_tree.remove(1)
    assert list(empty_tree) == [3]
    empty_tree.remove(3)
    assert list(empty_tree) == []


def test_iter2(filled_tree):
    assert list(filled_tree) == [2, 3, 4, 5, 6, 7, 8]
    filled_tree.remove(2)
    assert list(filled_tree) == [3, 4, 5, 6, 7, 8]
    filled_tree.remove(8)
    assert list(filled_tree) == [3, 4, 5, 6, 7]
    filled_tree.remove(5)
    assert list(filled_tree) == [3, 4, 6, 7]
    filled_tree.remove(3)
    assert list(filled_tree) == [4, 6, 7]
    filled_tree.remove(7)
    assert list(filled_tree) == [4, 6]
    filled_tree.remove(6)
    assert list(filled_tree) == [4]
    filled_tree.remove(4)
    assert list(filled_tree) == []


def test_add_single_element(empty_tree):
    empty_tree.add(1)
    assert empty_tree._length == 1
    assert empty_tree._size == 1
    assert empty_tree._min_element == 1
    assert empty_tree._max_element == 1
    assert empty_tree.count(1) == 1
    assert 1 in empty_tree


def test_add_same_element_twice(empty_tree):
    empty_tree.add(1)
    empty_tree.add(1)
    assert empty_tree._length == 2
    assert empty_tree._size == 1
    assert empty_tree._min_element == 1
    assert empty_tree._max_element == 1
    assert empty_tree.count(1) == 2
    assert 1 in empty_tree


def test_remove_last_element(empty_tree):
    empty_tree.add(1)
    empty_tree.remove(1)
    assert empty_tree._length == 0
    assert empty_tree._size == 0
    assert empty_tree._min_element is None
    assert empty_tree._max_element is None
    assert empty_tree.count(1) == 0
    assert 1 not in empty_tree


def test_remove_element(filled_tree):
    list_represenation_before = list(filled_tree)
    list_represenation_before.remove(3)
    filled_tree.remove(3)
    list_represenation_after = list(filled_tree)
    assert filled_tree._length == 6
    assert filled_tree._size == 6
    assert filled_tree._min_element == 2
    assert filled_tree._max_element == 8
    assert filled_tree.count(3) == 0
    assert 3 not in filled_tree
    assert list_represenation_before == list_represenation_after


def test_remove_duplicate(filled_tree):
    filled_tree.add(3)
    filled_tree.remove(3)
    assert filled_tree._length == 7
    assert filled_tree._size == 7
    assert filled_tree._min_element == 2
    assert filled_tree._max_element == 8
    assert filled_tree.count(3) == 1
    assert 3 in filled_tree


def test_random_add_remove():
    tree = MultiUnbalancedTree()
    list_representation = []
    for _ in range(100):
        value = random.randint(0, 100)
        if value not in list_representation:
            tree.add(value)
            list_representation.append(value)
        else:
            tree.remove(value)
            list_representation.remove(value)
        assert tree._length == len(list_representation)
        assert tree._size == len(set(list_representation))
        assert tree._min_element == (min(list_representation) if list_representation else None)
        assert tree._max_element == (max(list_representation) if list_representation else None)
        for value in list_representation:
            assert tree.count(value) == list_representation.count(value)
            assert value in tree
        for value in range(101):
            assert tree.count(value) == list_representation.count(value)
            assert (value in tree) == (value in list_representation)
        assert list(tree) == sorted(list_representation)
        assert list(MultiUnbalancedTree(tree)) == sorted(list_representation)
        assert list(MultiUnbalancedTree(list_representation)) == sorted(list_representation)


def test_random_add_remove_multiple():
    for _ in range(100):
        test_random_add_remove()


def test_lower_bound(filled_tree):
    assert filled_tree.lower_bound(1) == 2
    assert filled_tree.lower_bound(2) == 2
    assert filled_tree.lower_bound(3) == 3
    assert filled_tree.lower_bound(4) == 4
    assert filled_tree.lower_bound(5) == 5
    assert filled_tree.lower_bound(6) == 6
    assert filled_tree.lower_bound(7) == 7
    assert filled_tree.lower_bound(8) == 8
    assert filled_tree.lower_bound(9) is None
    assert filled_tree.lower_bound(10) is None


def test_upper_bound(filled_tree):
    assert filled_tree.upper_bound(1) == 2
    assert filled_tree.upper_bound(2) == 3
    assert filled_tree.upper_bound(3) == 4
    assert filled_tree.upper_bound(4) == 5
    assert filled_tree.upper_bound(5) == 6
    assert filled_tree.upper_bound(6) == 7
    assert filled_tree.upper_bound(7) == 8
    assert filled_tree.upper_bound(8) is None
    assert filled_tree.upper_bound(9) is None
    assert filled_tree.upper_bound(10) is None
