"""
Multiset implementation of an unbalanced tree.

Author: Andrei Lupasco
"""


class MultiUnbalancedTree:
    # internal node class
    class Node:
        def __init__(self, value, count=1, left=None, right=None):
            self.value = value
            self.count = count
            self.left = left
            self.right = right

    def __init__(self, elems=[]):
        """
        Creates a new empty tree.
        If an iterable is passed, the tree is initialized with its values.
        Parameters:
            elems: The iterable to initialize the tree with. Defaults to an empty tree.
        """
        self._root = None
        self._size = 0  # number of distinct elements
        self._length = 0  # number of elements
        self._min_element = None
        self._max_element = None

        # add the elements to the tree
        for elem in elems:
            self.add(elem)

    def _find(self, value, nil_node=None):
        """
        Returns the node with the given value or None if not found.
        The method uses the __eq__ method of the value to compare.
        Parameters:
            value: The value to search for.
        Returns:
            The node with the given value or None if not found.
        """

        node = self._root
        while node is not nil_node:
            # if the value is found, return the node
            if node.value == value:
                return node

            # otherwise, go left or right
            if node.value > value:
                node = node.left
            else:
                node = node.right

        # default return value
        return None

    def _add(self, value):
        """
        Adds a value to the tree.
        If the value already exists, the counter is increased.
        Parameters:
            value: The value to add.
        """

        # update the size
        self._length += 1

        # if the tree is empty, add the value as the root
        if self._root is None:
            self._root = self.Node(value)
            self._min_element = value
            self._max_element = value
            self._size = 1
            return

        # update the min and max elements
        if value < self._min_element:
            self._min_element = value
        if value > self._max_element:
            self._max_element = value

        # look for the value in the tree
        # if found, increase the counter
        # otherwise, add it to the tree

        node = self._root
        parent = None

        while node is not None:
            # if the value is found, increase the counter
            if node.value == value:
                node.count += 1
                return

            # otherwise, go left or right
            parent = node
            if node.value > value:
                node = node.left
            else:
                node = node.right

        # if the node is None, add the value
        else:
            self._size += 1
            if parent.value > value:
                parent.left = self.Node(value)
            else:
                parent.right = self.Node(value)
            return

    def _remove_node(self, node, parent):
        """
        Removes a node from the tree.
        Parameters:
            node: The node to remove.
            parent: The parent of the node to remove.
        """
        self._size -= 1

        # if the node has no children, simply remove it
        if node.left is None and node.right is None:
            if node is self._root:
                self._root = None
            elif parent.left is node:
                parent.left = None
            else:
                parent.right = None
            return

        # if the node has only one child, replace it with the child
        if node.left is None:
            if node is self._root:
                self._root = node.right
            elif parent.left is node:
                parent.left = node.right
            else:
                parent.right = node.right
            return
        if node.right is None:
            if node is self._root:
                self._root = node.left
            elif parent.left is node:
                parent.left = node.left
            else:
                parent.right = node.left
            return

        # if the node has two children, replace it with the leftmost leaf of the right subtree
        # and remove the leaf
        successor = node.right
        successor_parent = node

        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        node.value = successor.value
        node.count = successor.count

        if successor is successor_parent.left:
            successor_parent.left = successor.right
        else:
            successor_parent.right = successor.right

    def _remove(self, value):
        """
        Removes a value from the tree.
        If the value has a counter greater than 1, the counter is decreased.
        Otherwise, the value is removed from the tree.
        If the value is not found, raises a ValueError.
        Parameters:
            value: The value to remove.
        """

        node = self._root
        parent = None

        while node is not None:
            # if the value is found, decrease the counter
            if node.value == value:
                self._length -= 1
                if node.count > 1:
                    node.count -= 1
                else:
                    self._remove_node(node, parent)
                    # update the min and max elements
                    if self._length == 0:
                        self._min_element = None
                        self._max_element = None
                    elif value == self._min_element:
                        node = self._root
                        while node.left is not None:
                            node = node.left
                        self._min_element = node.value
                    elif value == self._max_element:
                        node = self._root
                        while node.right is not None:
                            node = node.right
                        self._max_element = node.value

                return

            # otherwise, go left or right
            parent = node
            if node.value > value:
                node = node.left
            else:
                node = node.right
        else:
            raise ValueError("Value not found.")

    def __contains__(self, value):
        """
        Checks if the tree contains a value.
        Parameters:
            value: The value to check.
        Returns:
            True if the value is in the tree, False otherwise.
        """

        return self._find(value) is not None

    def contains(self, value):
        """
        Checks if the tree contains a value.
        Parameters:
            value: The value to check.
        Returns:
            True if the value is in the tree, False otherwise.
        """

        return self._find(value) is not None

    def count(self, value):
        """
        Returns the number of occurrences of a value in the tree.
        Parameters:
            value: The value to count.
        Returns:
            The number of occurrences of the value in the tree.
        """

        node = self._find(value)
        if node is None:
            return 0
        return node.count

    def min(self):
        """
        Returns the minimum element in the tree.
        Returns:
            The minimum element in the tree.
        """

        return self._min_element

    def max(self):
        """
        Returns the maximum element in the tree.
        Returns:
            The maximum element in the tree.
        """

        return self._max_element

    def add(self, value):
        """
        Adds a value to the tree.
        Parameters:
            value: The value to add.
        """

        self._add(value)

    def remove(self, value):
        """
        Removes a value from the tree.
        If the value has a counter greater than 1, the counter is decreased.
        Otherwise, the value is removed from the tree.
        If the value is not found, raises a ValueError.
        Parameters:
            value: The value to remove.
        """

        self._remove(value)

    def __len__(self):
        """
        Returns the number of elements in the tree.
        Returns:
            The number of elements in the tree.
        """

        return self._length

    def __iter__(self, nil_node=None):
        """
        Returns a generator that yields the elements of the tree.
        """

        def inorder(node):
            if node is nil_node:
                return
            yield from inorder(node.left)
            for _ in range(node.count):
                yield node.value
            yield from inorder(node.right)

        return inorder(self._root)

    def __str__(self):
        """
        Returns a string representation of the tree.
        """

        return str(list(self))

    def __repr__(self):
        """
        Returns a string representation of the tree.
        """

        return str(list(self))

    def _lower_bound(self, value, nil_node):
        """
        Returns the smallest value that is greater than or equal to value.
        Parameters:
            value: The value to check.
        Returns:
            The lower bound of the value.
        """
        node = self._root
        result = None
        while node is not nil_node:
            if node.value == value:
                return node.value
            elif node.value < value:
                node = node.right
            else:
                result = node.value
                node = node.left
        return result

    def _upper_bound(self, value, nil_node):
        """
        Returns the smallest value that is greater than value.
        Parameters:
            value: The value to check.
        Returns:
            The upper bound of the value.
        """
        node = self._root
        result = None
        while node is not nil_node:
            if node.value <= value:
                node = node.right
            else:
                result = node.value
                node = node.left
        return result

    def lower_bound(self, value):
        """
        Returns the smallest value that is greater than or equal to value.
        Parameters:
            value: The value to check.
        Returns:
            The lower bound of the value.
        """
        return self._lower_bound(value, None)

    def upper_bound(self, value):
        """
        Returns the smallest value that is greater than value.
        Parameters:
            value: The value to check.
        Returns:
            The upper bound of the value.
        """
        return self._upper_bound(value, None)
