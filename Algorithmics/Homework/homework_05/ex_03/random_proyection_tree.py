import numpy as np
import sys
import matplotlib.pyplot as plt

MIN_NUM_BLOCKS_IN_LEAVE = 5

sys.setrecursionlimit(2000) # avoid recursion problems

def _random_vector(data):
    return np.random.randn(data.shape[1])

class Node:
    def __init__(self, data):
        self.random_vector = _random_vector(data)
        self.median = self.calculate_median(data)
        self.left = None
        self.right = None

    def calculate_median(self, data):
        dot_products = np.dot(data, self.random_vector)
        return np.median(dot_products)

    def divide_data(self, data):
        dot_products = np.dot(data, self.random_vector)
        left_data = data[dot_products < self.median]
        right_data = data[dot_products >= self.median]
        self.left = left_data
        self.right = right_data
        return left_data, right_data


def plot_tree(node):
    if node is None:
        return

    if node.left is not None:
        plt.scatter(node.left[:, 0], node.left[:, 1], color='blue', alpha=0.5, label='Left Points')
    if node.right is not None:
        plt.scatter(node.right[:, 0], node.right[:, 1], color='red', alpha=0.5, label='Right Points')

    plt.savefig(f'rp_tree_{num_nodes}.png')

num_nodes = 0

def create_rp_tree(data, depth=0, max_depth=20):

    global num_nodes
    # base case
    if len(data) <= MIN_NUM_BLOCKS_IN_LEAVE or depth >= max_depth:
        return Node(data)


    current_node = Node(data)
    num_nodes += 1
    left_data, right_data = current_node.divide_data(data)

    # plot_tree(current_node) uncomment to see the plots, leave pause
    # plt.pause(0.5)

    if len(left_data) > MIN_NUM_BLOCKS_IN_LEAVE:
        current_node.left = create_rp_tree(left_data, depth + 1, max_depth)
    if len(right_data) > MIN_NUM_BLOCKS_IN_LEAVE:
        current_node.right = create_rp_tree(right_data, depth + 1, max_depth)

    return current_node, num_nodes