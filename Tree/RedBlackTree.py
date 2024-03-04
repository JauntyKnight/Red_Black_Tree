"""
Set implementation using a red-black tree.
Internally its implemented as a MultiRedBlackTree with an overhead of checking
for duplicates before adding a value.
"""

from MultiRedBlackTree import MultiRedBlackTree


class RedBlackTree(MultiRedBlackTree):
    def __init__(self, elems=[]):
        """
        Creates a new RedBlackTree.
        Parameters:
            elems: An iterable of elements to add to the tree. Defaults to an empty tree.
        """
        super().__init__(elems)

    def add(self, value):
        """
        Adds a value to the tree.
        If the value is already in the tree, it is not added again.
        Parameters:
            value: The value to add.
        """
        if value not in self:
            super().add(value)

    def _draw_node(self, node, graph):
        """
        Adds a node to the graph.
        Parameters:
            node: The node to add.
            graph: The graph to add the node to.
        """
        if node.color == self.RED:
            graph.node(str(node.value), f"{node.value}", color="red")
        else:
            graph.node(str(node.value), f"{node.value}", color="black")
