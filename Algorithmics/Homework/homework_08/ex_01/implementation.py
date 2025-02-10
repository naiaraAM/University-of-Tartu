import networkx as nx
from collections import deque

def read_words(filename):
    """Read words from a file and return a list."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def compute_distance(word1, word2):
    """Compute the distance between two words as per the given formula."""
    len_diff = abs(len(word1) - len(word2))
    differences = len_diff
    min_len = min(len(word1), len(word2))
    for c1, c2 in zip(word1[:min_len], word2[:min_len]):
        if c1 != c2:
            differences += 1
    return 2 * differences - 1

def build_graph(words):
    """Build a graph where nodes are words and edges connect words with distance 1."""
    G = nx.Graph()
    G.add_nodes_from(words)
    total_words = len(words)
    for i in range(total_words):
        for j in range(i + 1, total_words):
            word1 = words[i]
            word2 = words[j]
            distance = compute_distance(word1, word2)
            if distance == 1:
                G.add_edge(word1, word2)
    return G

def dfs_longest_path(graph, start_node):
    """Perform DFS to find the longest path."""
    visited = set()
    stack = [(start_node, [start_node])]
    longest_path = []

    while stack:
        (vertex, path) = stack.pop()
        visited.add(vertex)
        for neighbor in set(graph.neighbors(vertex)) - visited:
            stack.append((neighbor, path + [neighbor]))
            if len(path) + 1 > len(longest_path):
                longest_path = path + [neighbor]

    return longest_path

def bfs_longest_path(graph, start_node):
    """Perform BFS to find the longest path."""
    visited = set()
    queue = deque([(start_node, [start_node])])
    longest_path = []

    while queue:
        (vertex, path) = queue.popleft()
        visited.add(vertex)
        for neighbor in set(graph.neighbors(vertex)) - visited:
            queue.append((neighbor, path + [neighbor]))
            if len(path) + 1 > len(longest_path):
                longest_path = path + [neighbor]

    return longest_path

def main():
    filenames = ['../words.5all.txt', '../words.5common.txt', '../words5.txt']
    for filename in filenames:
        words = read_words(filename)

        G = build_graph(words)

        # --- Characterize the Graph ---
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        num_components = nx.number_connected_components(G)
        print(f"Number of nodes: {num_nodes}")
        print(f"Number of edges: {num_edges}")
        print(f"Number of connected components: {num_components}")

        # Get all connected components and sort them by size
        components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
        components.sort(key=lambda c: c.number_of_nodes(), reverse=True)

        # Get the largest component
        largest_component = components[0]
        print(f"Largest Connected Component: {largest_component.number_of_nodes()} nodes, {largest_component.number_of_edges()} edges")

        dfs_path = dfs_longest_path(largest_component, list(largest_component.nodes())[0])
        print(f"Longest path using DFS: {len(dfs_path)} nodes")
        print(f"Width of DFS tree: {max(len(list(largest_component.neighbors(node))) for node in dfs_path)}")

        bfs_path = bfs_longest_path(largest_component, list(largest_component.nodes())[0])
        print(f"Longest path using BFS: {len(bfs_path)} nodes")
        print(f"Width of BFS tree: {max(len(list(largest_component.neighbors(node))) for node in bfs_path)}")

        diameter = nx.diameter(largest_component)
        print(f"Diameter of the largest component: {diameter}")
        print()

if __name__ == '__main__':
    main()
