"""
Set implementation using an unbalanced binary tree.
Internally its implemented as a MultiUnbalancedTree with an overhead of checking
for duplicates before adding a value.
"""

from MultiUnbalancedTree import MultiUnbalancedTree


class UnbalancedTree(MultiUnbalancedTree):
    def __init__(self, elems=[]):
        """
        Create a new UnbalancedTree.
        Parameters:
            elems: An iterable of elements to add to the tree.
        """
        super().__init__(elems)

    def add(self, value):
        """
        Add a value to the tree.
        If the value is already in the tree, it is not added again.
        Parameters:
            value: The value to add.
        """
        if value not in self:
            super().add(value)
