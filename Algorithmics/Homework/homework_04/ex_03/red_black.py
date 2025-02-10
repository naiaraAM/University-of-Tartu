import networkx as nx
import matplotlib.pyplot as plt

# Constants for indices in the node
INFO = 0
LEFT = 1
RIGHT = 2
PARENT = 3
COLOR = 4
NULL = 0  # Using 0 as null

# Initialize the tree array
def initialize_tree(size=1001):
    tree = [[0, 0, 0, 0, 'black'] for _ in range(size)]  # Initialize with 1001 nodes (index 0 + 1000 free nodes)
    tree[0][LEFT] = NULL  # Root starts as empty (0)
    tree[0][RIGHT] = 1  # Free list starts at node 1
    tree[0][PARENT] = NULL  # Free list starts at node 1
    for i in range(1, size - 1):
        tree[i][RIGHT] = i + 1  # Link all free nodes
    tree[size - 1][RIGHT] = NULL  # Last free node points to null
    return tree



# Allocate a new node from the free list
def allocate_node(tree):
    free_head = tree[0][RIGHT]
    """
    if free_head == NULL:
        expand_tree(tree)  # If no free nodes, expand the tree
        free_head = tree[0][RIGHT]
    """
    tree[0][RIGHT] = tree[free_head][RIGHT]  # Move the free list head to the next node
    tree[free_head] = [0, NULL, NULL,NULL, '']  # Reset the new node
    return free_head



def check_insert(tree, node, index):
    print(node)
    changed = False
    if node[PARENT] == NULL and node[COLOR] == 'red': # Case 0
        changed = True
        print(f"Case 0")
        node[COLOR] = 'black'
        tree[index] = node
        return
    parent, parent_index = tree[node[PARENT]], node[PARENT]
    print(f"Parent: {parent}")
    grandparent, grandparent_index = tree[parent[PARENT]], parent[PARENT]
    print(f"Grandparent: {grandparent}")
    uncle = None
    if grandparent[LEFT] == tree[index][PARENT]:
        uncle = tree[grandparent[RIGHT]]
    else:
        uncle = tree[grandparent[LEFT]]
    uncle_index = grandparent[LEFT] if grandparent[RIGHT] == parent_index else grandparent[RIGHT]
    print(f"Uncle: {uncle}")
    if uncle[COLOR] == 'red': # Case 1
        changed = True
        print(f"Case 1")
        parent[COLOR] = 'black'
        uncle[COLOR] = 'black'
    else: # Case 2 and 3, black uncle
        if parent[COLOR] != 'red':
            return False
         
        if parent[RIGHT] == index and parent[LEFT] == NULL and grandparent[LEFT] == parent_index: # rotate right
            print(f"Case 2, left pyramid")
            changed = True
            grandparent[LEFT] = index
            parent[RIGHT] = NULL
            parent[PARENT] = index
            node[LEFT] = parent_index
            node[PARENT] = grandparent_index
        
        elif parent[LEFT] == index and parent[RIGHT] == NULL and grandparent[RIGHT] == parent_index: # rotate left
            print(f"Case 2, right pyramid")
            changed = True
            grandparent[RIGHT] = index
            parent[LEFT] = NULL
            parent[PARENT] = index
            node[RIGHT] = parent_index
            node[PARENT] = grandparent_index
        # Case 3
        elif parent[LEFT] == index and grandparent[LEFT] == parent_index:
            print(f"Case 3, left line")
            changed = True
            grand_grandparent, grand_grandparent_index  = tree[grandparent[PARENT]], grandparent[PARENT]
            sibling, sibling_index = tree[parent[RIGHT]], parent[RIGHT]
            print(f"Sibling: {sibling}")
            print(f"Grand_grandparent: {grand_grandparent}")
            grand_grandparent[RIGHT] = parent_index
            parent[PARENT] = grand_grandparent_index
            grandparent[LEFT] = sibling_index
            sibling[PARENT] = grandparent_index
            parent[RIGHT] = grandparent_index
            grandparent[PARENT] = parent_index
            if parent[COLOR] == 'red':
                parent[COLOR] = 'black'
            if grandparent[COLOR] == 'black':
                grandparent[COLOR] = 'red'

        elif parent[RIGHT] == index and grandparent[RIGHT] == parent_index:
            print(f"Case 3, right line")
            grand_grandparent, grand_grandparent_index = tree[grandparent[PARENT]], grandparent[PARENT]
            sibling, sibling_index = tree[parent[LEFT]], parent[LEFT]
            grand_grandparent[LEFT] = parent_index
            parent[PARENT] = grand_grandparent_index
            grandparent[RIGHT] = sibling_index
            sibling[PARENT] = grandparent_index
            parent[LEFT] = grandparent_index
            grandparent[PARENT] = parent_index
            if parent[COLOR] == 'red':
                parent[COLOR] = 'black'
            else:
                parent[COLOR] = 'red'
            if grandparent[COLOR] == 'black':
                grandparent[COLOR] = 'red'
            else:
                grandparent[COLOR] = 'red'
    return changed


def check_tree(tree):
    changed = True
    while changed:
        changed = False
        for i in range(1, len(tree)):
            check = check_insert(tree, tree[i], i)
            if check:
                changed = True
                break
        
        
# Insert a new node into the tree
def insert_node(tree, value, color='red'):
    new_node = allocate_node(tree)
    tree[new_node][INFO] = value
    tree[new_node][COLOR] = color

    # Insert into the tree (binary search tree logic for simplicity)
    root = tree[0][LEFT]
    if root == NULL:
        tree[0][LEFT] = new_node  # Set the root if the tree is empty
    else:
        current = root
        while True:
            if value < tree[current][INFO]:  # Go to the left
                if tree[current][LEFT] == NULL:
                    tree[new_node][PARENT] = current
                    tree[current][LEFT] = new_node
                    break
                else:
                    current = tree[current][LEFT]
            else:  # Go to the right
                if tree[current][RIGHT] == NULL:
                    tree[new_node][PARENT] = current
                    tree[current][RIGHT] = new_node
                    break
                else:
                    current = tree[current][RIGHT]
    #visualize_tree(tree)
    check_insert(tree, tree[new_node], new_node)

    check_tree(tree)
    visualize_tree(tree) #uncomment to visualize the tree after each insertion
    

# In-order traversal to display the tree
def inorder_traversal(tree, node):
    if node == NULL:
        return
    inorder_traversal(tree, tree[node][LEFT])
    # print(f"Node {node}: Info={tree[node][INFO]}, Color={tree[node][COLOR]}, Left={tree[node][LEFT]}, Right={tree[node][RIGHT]}")
    inorder_traversal(tree, tree[node][RIGHT])

# Pre-order traversal to display the tree
def preorder_traversal(tree, node):
    if node == NULL:
        return
    # print(f"Node {node}: Info={tree[node][INFO]}, Color={tree[node][COLOR]}, Left={tree[node][LEFT]}, Right={tree[node][RIGHT]}")
    preorder_traversal(tree, tree[node][LEFT])
    preorder_traversal(tree, tree[node][RIGHT])

# Visualization function using networkx with hierarchical tree layout

def visualize_tree(tree):
    G = nx.DiGraph()  # Directed graph for tree
    root = tree[0][LEFT]
    pos = {}  # Dictionary to store positions of nodes

    def add_edges(node, x=0, y=0, x_offset=1):
        if node == NULL:
            return
        pos[tree[node][INFO]] = (x, y)  # Assign position based on x and y coordinates
        left_child = tree[node][LEFT]
        right_child = tree[node][RIGHT]

        if left_child != NULL:
            G.add_edge(tree[node][INFO], tree[left_child][INFO])
            add_edges(left_child, x - x_offset, y - 1, x_offset / 2)  # Move left child to the left
        if right_child != NULL:
            G.add_edge(tree[node][INFO], tree[right_child][INFO])
            add_edges(right_child, x + x_offset, y - 1, x_offset / 2)  # Move right child to the right

    # Start adding edges from the root
    add_edges(root)

    # Get colors for nodes based on their color attribute, not on pos order
    node_colors = []
    for key in pos.keys():
        for node in tree:
            if node[INFO] == key and node[INFO] != NULL:
                if node[COLOR] == 'red':
                    node_colors.append('lightcoral')
                else:
                    node_colors.append('grey')
                    break


    # Draw the tree with specified positions
    nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_weight="bold", arrows=True)
    plt.savefig(f"tree_{len(pos)}.png")
    plt.show()


ct = initialize_tree()

def next_collatz(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1

# collatz of 51 array
n = 7
insert_node(ct, n)
while n > 1:
    n = next_collatz(n)
    insert_node(ct, n)
    print(f"Inserted {n}")
    print("")
visualize_tree(ct)