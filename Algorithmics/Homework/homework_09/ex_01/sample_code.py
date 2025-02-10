import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from Homework.homework_09.ex_01.new_measure import closeness_centrality


def characterize_graph(G, graph_name):
    """Print basic properties of the graph."""
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = float(sum(dict(G.degree()).values())) / num_nodes
    density = nx.density(G)
    avg_clustering = nx.average_clustering(G)
    if G.is_directed():
        is_connected = nx.is_weakly_connected(G)
        components = nx.number_weakly_connected_components(G)
    else:
        is_connected = nx.is_connected(G)
        components = nx.number_connected_components(G)
    print(f"\nGraph: {graph_name}")
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")
    print(f"Average degree: {avg_degree:.2f}")
    print(f"Density: {density:.4f}")
    print(f"Average clustering coefficient: {avg_clustering:.4f}")
    print(f"Is connected: {is_connected}")
    print(f"Number of connected components: {components}")



def visualize_graph(G, graph_name):
    """Visualize the graph."""
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  # Position nodes using Fruchterman-Reingold force-directed algorithm
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', edge_color='gray')
    plt.title(f"Graph Visualization: {graph_name}")
    plt.show()

def run_pagerank(G, graph_name):
    """Run PageRank algorithm and output top-5 nodes."""
    pagerank_scores = nx.pagerank(G)
    # Sort nodes by PageRank score in descending order
    sorted_pagerank = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 5 nodes by PageRank in {graph_name}:")
    print("Rank\tNode\tPageRank Score\tDegree")
    for i, (node, score) in enumerate(sorted_pagerank[:10], start=1):
        degree = G.degree(node)
        print(f"{i}\t{node}\t{score:.6f}\t{degree}")

def plot_degree_distribution(G, graph_name):
    """Plot the degree distribution of the graph."""
    degrees = [d for n, d in G.degree()]
    plt.figure()
    plt.hist(degrees, bins=range(min(degrees), max(degrees)+1), align='left', edgecolor='black')
    plt.title(f'Degree Distribution: {graph_name}')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.show()

def detect_and_visualize_communities(G, graph_name):
    """Detect communities and visualize the graph with community coloring."""
    from networkx.algorithms import community
    # Use Girvan-Newman method for community detection
    communities_generator = community.girvan_newman(G)
    # Get the first level of communities
    top_level_communities = next(communities_generator)
    communities = [list(c) for c in top_level_communities]
    # Assign a community number to each node
    node_community = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node_community[node] = i
    # Visualization
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    colors = [node_community[node] for node in G.nodes()]
    nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.tab20)
    plt.title(f"Community Visualization: {graph_name}")
    plt.show()

def create_custom_graph():
    """Create a custom graph with explicit node and edge data."""
    G = nx.Graph()

    # Define nodes
    nodes = [1, 2, 3, 4, 5, 6, 7]
    G.add_nodes_from(nodes)

    # Define edges with optional weights or attributes
    edges = [
        (1, 2),
        (1, 3),
        (2, 3),
        (2, 4),
        (3, 5),
        (4, 5),
        (4, 6),
        (5, 6),
        (6, 7),
    ]
    G.add_edges_from(edges)

    # Optionally, add edge weights or other attributes
    # For example, adding weights to edges
    edge_weights = {
        (1, 2): 1.0,
        (1, 3): 2.0,
        (2, 3): 1.5,
        (2, 4): 2.5,
        (3, 5): 1.0,
        (4, 5): 2.0,
        (4, 6): 1.0,
        (5, 6): 1.5,
        (6, 7): 2.0,
    }
    nx.set_edge_attributes(G, edge_weights, 'weight')

    return G



def create_custom_graph_from_edge_list(edge_list_str):


    """Create a custom graph from an edge list string."""
    G = nx.Graph()
    for line in edge_list_str.strip().split('\n'):
        parts = line.strip().split()
        if len(parts) == 3:
            u, v, weight = parts
            G.add_edge(int(u), int(v), weight=float(weight))
        else:
            u, v = parts
            G.add_edge(int(u), int(v))
    return G

def my_example():

    return  """
1 2 1.0
1 3 2.0
2 3 1.5
2 4 2.5
3 5 1.0
4 5 2.0
4 6 1.0
5 6 1.5
6 7 2.0
6 3 7
6 8 9
"""


def main():

    edge_list_str = my_example()

    n_values = [30, 60, 120, 240]
    graphs = []
    for n in n_values:
        graphs.append(('Erdős-Rényi Graph', nx.erdos_renyi_graph(n=n, p=0.2, seed=42)))

    # # List of graphs with their names
    # graphs = [
    #     #('Karate Club Graph', nx.karate_club_graph()),
    #     #('Les Misérables Graph', nx.les_miserables_graph()),
    #     # ('Lollipop Graph', nx.lollipop_graph(m=10, n=5)),
    #     ('Erdős-Rényi Graph', nx.erdos_renyi_graph(n=30, p=0.2, seed=42)),
    #     ('Erdős-Rényi Graph', nx.erdos_renyi_graph(n=30, p=0.1, seed=42)),
    #     # ('Erdős-Rényi Graph 100 20%', nx.erdos_renyi_graph(n=100, p=0.2, seed=42)),
    #     # ('Erdős-Rényi Graph 100 5%', nx.erdos_renyi_graph(n=100, p=0.05, seed=42)),
    #     # ('Barbell Graph', nx.barbell_graph(m1=10, m2=10)),
    #     # ('Barabási-Albert Graph', nx.barabasi_albert_graph(n=30, m=2, seed=42)),
    #     # ('Barabási-Albert Graph', nx.barabasi_albert_graph(n=30, m=2, seed=42)),
    #     # ('Watts-Strogatz Graph', nx.watts_strogatz_graph(n=30, k=4, p=0.1, seed=42)),
    #     # ('Random geometric', nx.random_geometric_graph(100, radius=0.15, seed=42) ),
    #     # ('Random Directed Graph', nx.gn_graph(n=30, seed=42)),
    #     # ('Custom Graph', create_custom_graph()),
    #     # ('Custom Graph from Edge List', create_custom_graph_from_edge_list(edge_list_str)),
    #
    # ]

    for graph_name, G in graphs:
        # Characterize basic properties
        characterize_graph(G, graph_name)
        # Visualize the graph
        visualize_graph(G, graph_name)
        # Plot degree distribution
        plot_degree_distribution(G, graph_name)
        # Run PageRank and output top-10 nodes
        run_pagerank(G, graph_name)
        # Detect and visualize communities
        detect_and_visualize_communities(G, graph_name)
        # Print closeness centrality
        closeness_centrality(G, graph_name)

if __name__ == "__main__":
    main()