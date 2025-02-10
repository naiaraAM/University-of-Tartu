import networkx as nx
def closeness_centrality(G, graph_name):
    """Calculate and print closeness centrality"""
    centrality = nx.closeness_centrality(G)
    sorted_centrality = sorted(centrality.items(), key=lambda  x: x[1], reverse=True)
    print(f"\nTop 5 nodes by Closeness Centrality in {graph_name}:")
    print(f"Rank\tNode\tCloseness Centrality")
    for i, (node, score) in enumerate(sorted_centrality[:5], start=1):
        print(f"{i}\t{node}\t{score:.6f}")