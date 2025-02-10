import random
import networkx as nx

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

def build_weighted_graph(words):
    """Build a weighted graph where nodes are words and edges have weights based on the distance formula."""
    G = nx.Graph()
    G.add_nodes_from(words)
    total_words = len(words)
    for i in range(total_words):
        for j in range(i + 1, total_words):
            word1 = words[i]
            word2 = words[j]
            distance = compute_distance(word1, word2)
            if distance > 0:
                G.add_edge(word1, word2, weight=distance)
    return G

def main():
    words = read_words('../words.5common.txt')
    words = read_words('../words5.txt')

    G = build_weighted_graph(words)

    # --- Characterize the Graph ---
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    num_components = nx.number_connected_components(G)

    # Get all connected components and sort them by size
    components = [G.subgraph(c).copy() for c in nx.connected_components(G)]
    components.sort(key=lambda c: c.number_of_nodes(), reverse=True)

    # Get the largest component
    largest_component = components[0]

    # --- Find the Shortest Weighted Path ---
    source_word = random.choice(list(largest_component.nodes))
    target_word = random.choice(list(largest_component.nodes))

    # Check if both words are in the graph
    if source_word in G and target_word in G:
        try:
            # Find the shortest path using NetworkX with weights
            path_nx = nx.shortest_path(G, source=source_word, target=target_word, weight='weight')
            path_length = nx.shortest_path_length(G, source=source_word, target=target_word, weight='weight')
            path_weight_value = nx.path_weight(G, path_nx, weight='weight')

            print(f"Shortest path from '{source_word}' to '{target_word}' using NetworkX with weights:")
            for i in range(len(path_nx) - 1):
                print(f"{path_nx[i]} -> {path_nx[i+1]} (weight: {G[path_nx[i]][path_nx[i+1]]['weight']})")
            print(f"Path length: {path_length}, path weight: {path_weight_value}")
        except nx.NetworkXNoPath:
            print(f"No path exists between '{source_word}' and '{target_word}'.")
    else:
        missing_words = [word for word in [source_word, target_word] if word not in G]
        print(f"The following word(s) are not in the graph: {', '.join(missing_words)}")

if __name__ == '__main__':
    main()