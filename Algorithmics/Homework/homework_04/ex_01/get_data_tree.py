from homework_04.red_black_trees import initialize_tree, insert_node, preorder_traversal, visualize_tree, NULL, LEFT, \
    RIGHT, INFO
from collections import defaultdict, deque


def tree_size(tree, node):
    """
    Returns the number od nodes in the tree
    """
    if node == NULL:
        return 0
    return 1 + tree_size(tree, tree[node][LEFT]) + tree_size(tree, tree[node][RIGHT])

def tree_depth(tree, node):
    """
    Returns the depth of the tree, which is the longest path from the root to a leaf node
    """
    if node == NULL:
        return 0
    return 1 + max(tree_depth(tree, tree[node][LEFT]), tree_depth(tree, tree[node][RIGHT]))

def tree_width_at_each_depth(tree, node, depth=0, widths=None):
    """
    Returns the width of the tree at each depth/level
    """
    if widths is None:
        widths = defaultdict(int)
    if node != NULL:
        widths[depth] += 1
        tree_width_at_each_depth(tree, tree[node][LEFT], depth + 1, widths)
        tree_width_at_each_depth(tree, tree[node][RIGHT], depth + 1, widths)
    return widths

def preorder(tree, node, result=None):
    """
    First visit the root, then the left subtree, and finally the right subtree
    """
    if result is None:
        result = []
    if node != NULL:
        result.append(tree[node][INFO])
        preorder(tree, tree[node][LEFT], result)
        preorder(tree, tree[node][RIGHT], result)
    return result

def inorder(tree, node, result=None):
    """
    First visit the left subtree, then the root, and finally the right subtree, resulting in a sorted list
    """
    if result is None:
        result = []
    if node != NULL:
        inorder(tree, tree[node][LEFT], result)
        result.append(tree[node][INFO])
        inorder(tree, tree[node][RIGHT], result)
    return result

def postorder(tree, node, result=None):
    """
    It visits the left subtree, then the right subtree, and finally the root
    """
    if result is None:
        result = []
    if node != NULL:
        postorder(tree, tree[node][LEFT], result)
        postorder(tree, tree[node][RIGHT], result)
        result.append(tree[node][INFO])
    return result

def serialize_tree(tree, node):
    """
    It returns a string representation of the tree
    """
    if node == NULL:
        return ""
    left = serialize_tree(tree, tree[node][LEFT])
    right = serialize_tree(tree, tree[node][RIGHT])
    return f"{tree[node][INFO]}({left},{right})"

def breadth_first_order(tree, root):
    """
    Breadth-first traversal of the tree, from root to leaves
    """
    if root == NULL:
        return []
    queue = deque([root])
    result = []
    while queue:
        node = queue.popleft()
        result.append(tree[node][INFO])
        if tree[node][LEFT] != NULL:
            queue.append(tree[node][LEFT])
        if tree[node][RIGHT] != NULL:
            queue.append(tree[node][RIGHT])
    return result



def get_data_tree(collatz_tree,
                  node,
                  size=False,
                  depth=False,
                  tree_width_of_depth=False,
                  preorder_var=False,
                  inorder_var=False,
                  postorder_var=False,
                  serialized_representation=False,
                  breadth_first_order_var=False):
    if size:
        return tree_size(collatz_tree, node)
    elif depth:
        return tree_depth(collatz_tree, node)
    elif tree_width_of_depth:
        return tree_width_at_each_depth(collatz_tree, node)
    elif preorder_var:
        return preorder(collatz_tree, node)
    elif inorder_var:
        return inorder(collatz_tree, node)
    elif postorder_var:
        return postorder(collatz_tree, node)
    elif serialized_representation:
        return serialize_tree(collatz_tree, node)
    elif breadth_first_order_var:
        return breadth_first_order(collatz_tree, node)


if __name__ == '__main__':
    n = [7, 9, 51]
    collatz_tree = initialize_tree()
    for n_val in n:
        insert_node(collatz_tree, n_val, 'red')
        while n_val > 1:
            n_val = n_val // 2 if n_val % 2 == 0 else 3 * n_val + 1
            insert_node(collatz_tree, n_val, 'red')
        node_n = collatz_tree[0][LEFT]
        print(get_data_tree(collatz_tree, node_n, size=True))
        print(get_data_tree(collatz_tree, node_n, depth=True))
        print(get_data_tree(collatz_tree, node_n, tree_width_of_depth=True))
        print(get_data_tree(collatz_tree, node_n, preorder_var=True))
        print(get_data_tree(collatz_tree, node_n, inorder_var=True))
        print(get_data_tree(collatz_tree, node_n, postorder_var=True))
        print(get_data_tree(collatz_tree, node_n, serialized_representation=True))
        print(get_data_tree(collatz_tree, node_n, breadth_first_order_var=True))
