from homework_04.red_black_trees import NULL, LEFT, RIGHT, INFO, initialize_tree, insert_node, next_collatz, \
    preorder_traversal


def find_max_path(tree):
    def max_path_sum(node):
        nonlocal max_sum, max_path
        if node == NULL:
            return 0, []

        left_sum, left_path = max_path_sum(tree[node][LEFT])  # max left sub tree
        right_sum, right_path = max_path_sum(tree[node][RIGHT])  # max right sub tree

        current_sum = tree[node][INFO] + left_sum + right_sum

        if current_sum > max_sum:
            max_sum = current_sum
            max_path = left_path + [tree[node][INFO]] + right_path

        # Return the maximum path sum including the current node
        if left_sum > right_sum:
            return tree[node][INFO] + left_sum, left_path + [tree[node][INFO]]
        else:
            return tree[node][INFO] + right_sum, right_path + [tree[node][INFO]]

    max_sum = float('-inf')
    max_path = []
    max_path_sum(tree[0][LEFT])
    return max_sum, max_path

def common_ancestor(tree, path):
    for i in range(len(tree)):
        if tree[i][LEFT] != NULL and tree[i][RIGHT] != NULL:
            if tree[i][INFO] in path and tree[tree[i][LEFT]][INFO] in path and tree[tree[i][RIGHT]][INFO] in path:
                return tree[i][INFO]
    return None


def print_max_path(tree, max_path, max_sum):
    if not max_path:
        return

    ancestor = common_ancestor(tree, max_path)
    common_index = max_path.index(ancestor) # common ancestor index

    left_path = max_path[:common_index]
    right_path = max_path[common_index + 1:]
    right_path = right_path[::-1] # reverse the right path


    combined_path = ', '.join(map(str, left_path)) + f", ({ancestor}), " + ', '.join(map(str, right_path))
    print(f"Max path: {combined_path}")

n = [7, 9, 51]
for n_val in n:
    tree = initialize_tree()
    insert_node(tree, n_val, 'red')
    while n_val > 1:
        n_val = next_collatz(n_val)
        insert_node(tree, n_val, 'red')

    preorder_traversal(tree, tree[0][LEFT])

    max_sum, max_path = find_max_path(tree)
    print(f"The maximum path sum is: {max_sum}")
    print_max_path(tree, max_path, max_sum)
