""""
Multiset implementation of a red-black tree.
Based on 'Introduction to Algorithms' by Cormen et al. 4th edition
"""

from MultiUnbalancedTree import MultiUnbalancedTree
from graphviz import Digraph


class MultiRedBlackTree(MultiUnbalancedTree):
    # internal node class
    class Node:
        def __init__(self, value, color, count=1):
            self.value = value
            self.count = count
            self.color = color
            self.left = self
            self.right = self
            self.parent = self

    def __init__(self, elems=[]):
        """
        Creates a new red-black tree.
        If an iterable is passed, the tree is initialized with its values.
        Parameters:
            elems: An iterable. Defaults to an empty tree.
        """
        self.RED = 0
        self.BLACK = 1
        self.NIL = self.Node(None, self.BLACK)
        self._root = self.NIL
        self._size = 0  # number of distinct elements
        self._length = 0  # number of elements
        self._min_element = None
        self._max_element = None

        for elem in elems:
            self.add(elem)

    def _left_rotate(self, node):
        """
        Performs a left rotation on the given node.
        Parameters:
            node: The node to rotate.
        """
        if node is self.NIL:
            return

        right = node.right
        node.right = right.left  # turn right's left subtree into node's right subtree
        if right.left is not self.NIL:  # if right's left subtree is not self.NIL
            right.left.parent = node  # update the parent
        right.parent = node.parent  # link node's parent to right
        if node.parent is self.NIL:  # if node was the root
            self._root = right  # right is the new root
        elif node is node.parent.left:  # if node was a left child
            node.parent.left = right  # update the parent
        else:  # if node was a right child
            node.parent.right = right  # update the parent
        right.left = node  # put node on right's left
        node.parent = right  # update the parent

    def _right_rotate(self, node):
        """
        Performs a right rotation on the given node.
        Parameters:
            node: The node to rotate.
        """

        # This check is not in the book but needed to avoid
        # self._T_root = y below.
        if node is self.NIL:
            return

        left = node.left
        node.left = left.right  # turn left's right subtree into node's left subtree
        if left.right is not self.NIL:  # if left's right subtree is not self.NIL
            left.right.parent = node  # update the parent
        left.parent = node.parent  # link node's parent to left
        if node.parent is self.NIL:  # if node was the root
            self._root = left  # left is the new root
        elif node is node.parent.right:  # if node was a right child
            node.parent.right = left  # update the parent
        else:  # if node was a left child
            node.parent.left = left  # update the parent
        left.right = node  # put node on left's right
        node.parent = left  # update the parent

    def _rb_insert_fixup(self, node):
        """
        Fixes the red-black tree properties after an insertion.
        Parameters:
            node: The node that was inserted.
        """

        while node.parent.color == self.RED:
            if node.parent is node.parent.parent.left:
                # node's parent is a left child
                uncle = node.parent.parent.right
                if uncle is not self.NIL and uncle.color == self.RED:
                    # case 1: uncle is red
                    node.parent.color = self.BLACK
                    uncle.color = self.BLACK
                    node.parent.parent.color = self.RED
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        # case 2: uncle is black and node is a right child
                        node = node.parent
                        self._left_rotate(node)
                    # case 3: uncle is black and node is a left child
                    node.parent.color = self.BLACK
                    node.parent.parent.color = self.RED
                    self._right_rotate(node.parent.parent)
            else:
                # same as above, but with left and right exchanged
                uncle = node.parent.parent.left
                if uncle is not self.NIL and uncle.color == self.RED:
                    # case 1
                    node.parent.color = self.BLACK
                    uncle.color = self.BLACK
                    node.parent.parent.color = self.RED
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        # case 2
                        node = node.parent
                        self._right_rotate(node)
                    # case 3
                    node.parent.color = self.BLACK
                    node.parent.parent.color = self.RED
                    self._left_rotate(node.parent.parent)

        self._root.color = self.BLACK

    def _add(self, value):
        """
        Adds a value to the tree.
        If the value already exists, the counter is increased.
        Parameters:
            value: The value to add.
        """

        self._length += 1

        node = self._root
        parent = self.NIL

        # find the place to insert the new node
        while node is not self.NIL:
            parent = node
            if node.value == value:
                node.count += 1
                return

            if node.value > value:
                node = node.left
            else:
                node = node.right

        # if reached here, the value is not in the tree
        self._size += 1
        new_node = self.Node(value, self.RED)
        new_node.parent = parent

        if parent is self.NIL:
            # the tree was empty
            self._root = new_node
            self._min_element = value
            self._max_element = value
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.left = self.NIL
        new_node.right = self.NIL

        self._min_element = min(self._min_element, value)
        self._max_element = max(self._max_element, value)

        try:
            self._rb_insert_fixup(new_node)
        except AttributeError:
            pass

    def _rb_transplant(self, node1, node2):
        """
        Replaces the subtree rooted at node1 with the subtree rooted at node2.
        Parameters:
            node1: The node to replace.
            node2: The node to replace with.
        """

        if node1.parent is self.NIL:
            self._root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2

        node2.parent = node1.parent

    def _rb_delete_fixup(self, node):
        """
        Fixes the red-black tree properties after a deletion.
        Parameters:
            node: The node that was deleted.
        """

        while node != self._root and node.color == self.BLACK:
            if node is node.parent.left:
                # node is a left child
                sibling = node.parent.right
                if sibling.color == self.RED:
                    # case 1: sibling is red
                    sibling.color = self.BLACK
                    node.parent.color = self.RED
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == self.BLACK and sibling.right.color == self.BLACK:
                    # case 2: sibling is black and both its children are black
                    sibling.color = self.RED
                    node = node.parent
                else:
                    if sibling.right.color == self.BLACK:
                        # case 3: sibling is black, its left child is red and its right child is black
                        sibling.left.color = self.BLACK
                        sibling.color = self.RED
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    # case 4: sibling is black and its right child is red
                    sibling.color = node.parent.color
                    node.parent.color = self.BLACK
                    sibling.right.color = self.BLACK
                    self._left_rotate(node.parent)
                    node = self._root
            else:
                # same as above, but with left and right exchanged
                sibling = node.parent.left
                if sibling.color == self.RED:
                    # case 1
                    sibling.color = self.BLACK
                    node.parent.color = self.RED
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                if sibling.right.color == self.BLACK and sibling.left.color == self.BLACK:
                    # case 2
                    sibling.color = self.RED
                    node = node.parent
                else:
                    if sibling.left.color == self.BLACK:
                        # case 3
                        sibling.right.color = self.BLACK
                        sibling.color = self.RED
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    # case 4
                    sibling.color = node.parent.color
                    node.parent.color = self.BLACK
                    sibling.left.color = self.BLACK
                    self._right_rotate(node.parent)
                    node = self._root

        node.color = self.BLACK

    def _tree_minimum(self, node):
        """
        Returns the minimum node in the subtree rooted at node.
        Parameters:
            node: The root of the subtree.
        """

        while node.left is not self.NIL:
            node = node.left
        return node

    def _tree_maximum(self, node):
        """
        Returns the maximum node in the subtree rooted at node.
        Parameters:
            node: The root of the subtree.
        """

        while node.right is not self.NIL:
            node = node.right
        return node

    def _remove_node(self, node_to_delete):
        """
        Removes a node from the tree.
        Parameters:
            node_to_delete: The node to remove.
        """

        self._size -= 1

        if self._size == 0:
            self._root = self.NIL
            self._min_element = None
            self._max_element = None
            return

        node = node_to_delete
        original_color = node.color
        if node_to_delete.left is self.NIL:
            # node has no left child
            child = node_to_delete.right
            self._rb_transplant(node_to_delete, node_to_delete.right)
        elif node_to_delete.right is self.NIL:
            # node has no right child
            child = node_to_delete.left
            self._rb_transplant(node_to_delete, node_to_delete.left)
        else:
            # node has two children
            node = self._tree_minimum(node_to_delete.right)
            original_color = node.color
            child = node.right
            if node.parent is node_to_delete and child is not self.NIL:
                child.parent = node
            else:
                self._rb_transplant(node, node.right)
                node.right = node_to_delete.right
                node.right.parent = node
            self._rb_transplant(node_to_delete, node)
            node.left = node_to_delete.left
            node.left.parent = node
            node.color = node_to_delete.color

        if original_color == self.BLACK:
            self._rb_delete_fixup(child)

        if self._min_element == node_to_delete.value:
            self._min_element = self._tree_minimum(self._root).value
        if self._max_element == node_to_delete.value:
            self._max_element = self._tree_maximum(self._root).value

    def remove(self, value):
        """
        Removes a value from the tree.
        If the value has a counter greater than 1, the counter is decreased.
        Raises ValueError if the value is not in the tree.
        Parameters:
            value: The value to remove.
        """

        self._length -= 1
        node = self._root

        # find the node to remove
        while node is not self.NIL:
            if node.value == value:
                if node.count > 1:
                    node.count -= 1
                    return
                self._remove_node(node)
                return

            if node.value > value:
                node = node.left
            else:
                node = node.right
        else:
            raise ValueError("Value not found in tree")

    def _draw_node(self, node, graph):
        """
        Adds a node to the graph.
        Parameters:
            node: The node to add.
            graph: The graph to add the node to.
        """
        if node.color == self.RED:
            graph.node(str(node.value), f"{node.value}\n{node.count}", color="red")
        else:
            graph.node(str(node.value), f"{node.value}\n{node.count}", color="black")

    def draw(self, name="tree", view_nil=False):
        """
        Generates a pdf file with a visualization of the tree.
        Parameters:
            name: The name of the pdf file.
        """
        graph = Digraph()

        def draw_node(node):
            self._draw_node(node, graph)
            if node.left is not self.NIL:
                draw_node(node.left)
                graph.edge(str(node.value), str(node.left.value))
            elif view_nil:
                graph.node(str(node.value) + "l", "NIL", color="black")
                graph.edge(str(node.value), str(node.value) + "l")
            if node.right is not self.NIL:
                draw_node(node.right)
                graph.edge(str(node.value), str(node.right.value))
            elif view_nil:
                graph.node(str(node.value) + "r", "NIL", color="black")
                graph.edge(str(node.value), str(node.value) + "r")

        draw_node(self._root)
        graph.render(name, view=True, cleanup=True)

    def is_red_black(self):
        """
        Checks if the tree is a valid red-black tree.
        Returns:
            True if the tree is a valid red-black tree, False otherwise.
        """

        def check_colors(node):
            if node is self.NIL:
                return True
            if node.color == self.RED:
                if node.left is not self.NIL and node.left.color == self.RED:
                    return False
                if node.right is not self.NIL and node.right.color == self.RED:
                    return False
            return check_colors(node.left) and check_colors(node.right)

        def check_black_height(node):
            if node is self.NIL:
                return 0
            left_height = check_black_height(node.left)
            right_height = check_black_height(node.right)
            if left_height != right_height:
                return -1
            return left_height + (1 if node.color == self.BLACK else 0)

        return check_colors(self._root) and check_black_height(self._root) != -1

    def __iter__(self):
        """
        Returns a generator that iterates over the tree in order.
        """
        return super().__iter__(self.NIL)

    def _find(self, value):
        """
        Returns the node with the given value.
        If no such node exists, returns self.NIL.
        """
        return super()._find(value, self.NIL)

    def lower_bound(self, value):
        """
        Returns the smallest value in the tree that is greater than or equal to the given value.
        If no such value exists, returns None.
        Parameters:
            value: The value to compare to.
        """
        return super()._lower_bound(value, self.NIL)

    def upper_bound(self, value):
        """
        Returns the smallest value in the tree that is greater than the given value.
        If no such value exists, returns None.
        Parameters:
            value: The value to compare to.
        """
        return super()._upper_bound(value, self.NIL)

    def _count_size(self, node):
        """
        Returns the size of the subtree rooted at node.
        Parameters:
            node: The root of the subtree.
        """
        if node is self.NIL:
            return 0
        return node.count + self._count_size(node.left) + self._count_size(node.right)
