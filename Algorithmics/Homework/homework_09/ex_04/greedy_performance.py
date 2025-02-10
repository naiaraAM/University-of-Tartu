import networkx as nx
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os

# Function to initialize the graph
def create_graph():
    G = nx.DiGraph()
    edges = [
        ('A', 'B', 10),
        ('A', 'C', 9),
        ('B', 'D', 200),
        ('B', 'E', 20),
        ('C', 'F', 1000),
        ('C', 'G', 50),
    ]
    G.add_weighted_edges_from(edges)
    return G


# Function to set up directories for saving frames
def setup_frame_directory():
    frame_dir = 'frames'
    if not os.path.exists(frame_dir):
        os.makedirs(frame_dir)
    return frame_dir


# Function to capture the current graph state as a frame
def capture_frame(G, pos, path, frame_dir, frames):
    plt.figure(figsize=(8, 6))
    node_colors = ['lightblue' if n not in path else 'lightgreen' for n in G.nodes()]
    edge_colors = ['gray' if (u, v) not in zip(path[:-1], path[1:]) else 'red' for u, v in G.edges()]

    # Draw the graph with edge weights
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=3000, font_size=15,
            width=2)
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='black')

    # Save the frame
    frame_path = os.path.join(frame_dir, f"frame_{len(frames)}.png")
    plt.savefig(frame_path)
    frames.append(frame_path)
    plt.close()


# Function to perform DFS and capture the path frames
def dfs(G, node, path, weight_sum, longest_path, longest_path_weight, pos, frame_dir, frames):
    # Capture the current frame
    capture_frame(G, pos, path, frame_dir, frames)

    # If the current node is a leaf (no outgoing edges), check the path's weight
    if len(list(G.neighbors(node))) == 0:
        if weight_sum > longest_path_weight:
            longest_path_weight = weight_sum
            longest_path = path.copy()  # Save the longest path
        return longest_path, longest_path_weight

    # Explore all neighbors
    for neighbor in G.neighbors(node):
        edge_weight = G[node][neighbor]['weight']
        path.append(neighbor)  # Add neighbor to path
        longest_path, longest_path_weight = dfs(G, neighbor, path, weight_sum + edge_weight, longest_path,
                                                longest_path_weight, pos, frame_dir, frames)
        path.pop()  # Backtrack

    return longest_path, longest_path_weight


def greedy(G, node, path, weight_sum, longest_path, longest_path_weight, pos, frame_dir, frames):
    capture_frame(G, pos, path, frame_dir, frames)

    # If the current node is a leaf (no outgoing edges), check the path's weight
    if len(list(G.neighbors(node))) == 0:  # "Optimal path found"
        if weight_sum > longest_path_weight:
            longest_path_weight = weight_sum
            longest_path = path.copy()  # Save the longest path
        return longest_path, longest_path_weight

    # List to store the neighbors and their associated edge weights
    neighbor_edges_weight = []
    for neighbor in G.neighbors(node):
        neighbor_edges_weight.append((neighbor, G[node][neighbor]['weight']))

    # Select the neighbor with the maximum edge weight
    best_neighbor, best_weight = max(neighbor_edges_weight, key=lambda x: x[1])

    # Add the best neighbor to the path and recursively call greedy on that neighbor
    path.append(best_neighbor)  # Add the selected neighbor to the path
    longest_path, longest_path_weight = greedy(G, best_neighbor, path, weight_sum + best_weight,
                                               longest_path, longest_path_weight, pos, frame_dir, frames)
    path.pop()  # Backtrack

    return longest_path, longest_path_weight




# Function to add the longest path as the final frame
def add_longest_path_frame(G, longest_path, pos, frame_dir, frames):
    plt.figure(figsize=(8, 6))
    node_colors = ['lightblue' if n not in longest_path else 'lightgreen' for n in G.nodes()]
    edge_colors = ['gray' if (u, v) not in zip(longest_path[:-1], longest_path[1:]) else 'red' for u, v in G.edges()]

    # Draw the graph with the longest path highlighted
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=3000, font_size=15,
            width=2)
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='black')

    # Capture the final frame with the longest path highlighted
    frame_path = os.path.join(frame_dir, f"frame_{len(frames)}.png")
    plt.savefig(frame_path)
    frames.append(frame_path)
    plt.close()


# Function to create the animation from frames
def create_animation(frames, mode):
    if mode:
        with imageio.get_writer('dfs_steps.gif', mode='I', duration=3.0, loop=0) as writer:
            for frame_path in frames:
                frame = imageio.imread(frame_path)
                for _ in range(300):  # Repeat each frame 120 times
                    writer.append_data(frame)
    else:
        with imageio.get_writer('greedy_steps.gif', mode='I', duration=3.0, loop=0) as writer:
            for frame_path in frames:
                frame = imageio.imread(frame_path)
                for _ in range(300):  # Repeat each frame 120 times
                    writer.append_data(frame)


# Function to clean up the temporary frame directory
def cleanup(frame_dir, frames):
    for frame_path in frames:
        os.remove(frame_path)
    os.rmdir(frame_dir)


# Main function to run the DFS and generate the animation
def main():
    # Step 1: Create the graph
    G = create_graph()

    # Step 2: Set up the frame directory
    frame_dir = setup_frame_directory()

    # Step 3: Set up variables for tracking the longest path
    longest_path = []
    longest_path_weight = float('-inf')

    # Step 4: Position for plotting
    pos = nx.spring_layout(G)

    # Step 5: List to store frames
    frames = []

    # Step 6: Start DFS from node 'A'
    longest_path, longest_path_weight = dfs(G, 'A', ['A'], 0, longest_path, longest_path_weight, pos, frame_dir, frames)

    # Step 7: Add the longest path frame at the end
    add_longest_path_frame(G, longest_path, pos, frame_dir, frames)

    # Step 8: Create an animation from the frames
    create_animation(frames, True)

    # Step 9: Clean up the temporary frame directory
    cleanup(frame_dir, frames)

    # Output the correct longest path and weight
    print(f"Longest path DFS: {longest_path} with weight {longest_path_weight}")

    # Step 1: Create the graph
    G = create_graph()

    # Step 2: Set up the frame directory
    frame_dir = setup_frame_directory()

    # Step 3: Set up variables for tracking the longest path
    longest_path = []
    longest_path_weight = float('-inf')

    # Step 4: Position for plotting
    pos = nx.spring_layout(G)

    # Step 5: List to store frames
    frames = []

    # Step 6: Start DFS from node 'A'
    longest_path, longest_path_weight = greedy(G, 'A', ['A'], 0, longest_path, longest_path_weight, pos, frame_dir, frames)

    # Step 7: Add the longest path frame at the end
    add_longest_path_frame(G, longest_path, pos, frame_dir, frames)

    # Step 8: Create an animation from the frames
    create_animation(frames, False)

    # Step 9: Clean up the temporary frame directory
    cleanup(frame_dir, frames)

    # Output the correct longest path and weight
    print(f"Longest path greedy: {longest_path} with weight {longest_path_weight}")

# Run the main function
if __name__ == "__main__":
    main()
