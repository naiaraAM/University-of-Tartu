import numpy as np
from PIL import Image, ImageDraw
import networkx as nx
import random
import os
import glob
import heapq
from collections import deque

def load_image(image_path):
    """Load the image and convert it to RGB array."""
    image = Image.open(image_path).convert('RGB')
    return np.array(image), image.size, image

def sample_pixels(rgb_array, Xstep=40, Ystep=40):
    """Sample pixels every 'Xstep' columns and 'Ystep' rows and compute average colors."""
    nodes = {}
    height, width, _ = rgb_array.shape
    for y in range(0, height, Ystep):
        for x in range(0, width, Xstep):
            # Get 3x3 surrounding pixels
            x_min = max(x - 1, 0)
            x_max = min(x + 2, width)
            y_min = max(y - 1, 0)
            y_max = min(y + 2, height)
            region = rgb_array[y_min:y_max, x_min:x_max]
            # Compute average color
            avg_color = region.mean(axis=(0, 1)).astype(int)
            # Node ID as tuple
            node_id = (x, y)
            nodes[node_id] = {
                'position': (x, y),
                'avg_color': tuple(avg_color)
            }
    return nodes

def create_graph(nodes, Xstep=40, Ystep=40):
    """Create a graph where each node is connected to its 8 neighbors."""
    G = nx.Graph()
    for node_id, data in nodes.items():
        G.add_node(node_id, **data)
    # Connect nodes to their 8 neighbors
    offsets = [(-Xstep, -Ystep), (-Xstep, 0), (-Xstep, Ystep),
               (0, -Ystep),    (0, Ystep),
               (Xstep, -Ystep), (Xstep, 0), (Xstep, Ystep)]
    for node_id, data in nodes.items():
        x, y = data['position']
        for dx, dy in offsets:
            neighbor_x = x + dx
            neighbor_y = y + dy
            neighbor_id = (neighbor_x, neighbor_y)
            if neighbor_id in nodes:
                G.add_edge(node_id, neighbor_id)
    return G

def calculate_edge_weights(G, rgb_array):
    """Calculate weights for edges based on pixel brightness along the line."""
    specific_color = np.array([255, 255, 0]) # set to green

    for u, v in G.edges():
        x1, y1 = G.nodes[u]['position']
        x2, y2 = G.nodes[v]['position']
        # Get pixels along the line
        pixels_on_line = get_line_pixels(x1, y1, x2, y2)
        weight = 0
        for x, y in pixels_on_line:
            # Ensure coordinates are within image bounds
            if 0 <= x < rgb_array.shape[1] and 0 <= y < rgb_array.shape[0]:
                r, g, b = rgb_array[y, x].astype(int)
                rgb_color = np.array([r, g, b])
                # Calculate speed based on color
                speed = 1.0
                if r > 200 or g > 200:  # Higher speed for red or green pixels
                    speed = 2.0
                # Adjust speed based on difference from specific color
                color_diff = np.linalg.norm(rgb_color - specific_color)
                speed += 1.0 / (color_diff + 1e-6)  # Avoid division by zero
                weight += 1 / speed
            else:
                weight += 1  # Assign a default value if out of bounds
        G.edges[u, v]['weight'] = weight
    return G

def get_line_pixels(x0, y0, x1, y1):
    """Bresenham's Line Algorithm to get all pixels between two points."""
    pixels = []
    x0 = int(round(x0))
    y0 = int(round(y0))
    x1 = int(round(x1))
    y1 = int(round(y1))
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx == 0 and dy == 0:
        return [(x0, y0)]
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            pixels.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            pixels.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    pixels.append((x1, y1))
    return pixels

def draw_graph(G, original_image, bbox_size=2):
    """Overlay the graph onto the original image."""
    draw = ImageDraw.Draw(original_image)

    # Draw nodes
    for node_id, data in G.nodes(data=True):
        x, y = data['position']
        avg_color = data['avg_color']
        bbox = [x - bbox_size, y - bbox_size, x + bbox_size, y + bbox_size]
        draw.ellipse(bbox, fill=avg_color)

    # Calculate min and max weights for normalization
    weights = [data['weight'] for _, _, data in G.edges(data=True)]
    max_weight = max(weights)
    min_weight = min(weights)

    # Draw edges
    for u, v, data in G.edges(data=True):
        x1, y1 = G.nodes[u]['position']
        x2, y2 = G.nodes[v]['position']
        weight = data['weight']
        # Map weight to red intensity
        normalized_weight = (weight - min_weight) / (max_weight - min_weight + 1e-6)
        red_intensity = int(255 * (1 - normalized_weight))  # Invert to make lower weight darker
        line_color = (red_intensity, 0, 0)
        draw.line([x1, y1, x2, y2], fill=line_color)

    return original_image

def bfs_tree(G, start_node):
    """Perform BFS and return the BFS tree as a list of edges and node levels."""
    visited = set()
    queue = deque()
    parent = {}
    level = {}
    visited.add(start_node)
    queue.append((start_node, 0))  # Include level information
    parent[start_node] = None
    level[start_node] = 0
    bfs_edges = []
    while queue:
        current_node, current_level = queue.popleft()
        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, current_level + 1))
                parent[neighbor] = current_node
                level[neighbor] = current_level + 1
                bfs_edges.append((current_node, neighbor))
    return bfs_edges, level

# Add DFS tree traversal function
def dfs_tree(G, start_node):
    """Perform DFS and return the DFS tree as a list of edges and node levels."""
    visited = set()
    stack = [(start_node, 0)]
    parent = {}
    level = {}
    dfs_edges = []

    while stack:
        current_node, current_level = stack.pop()
        if current_node in visited:
            continue
        visited.add(current_node)
        level[current_node] = current_level

        for neighbor in G.neighbors(current_node):
            if neighbor not in visited:
                parent[neighbor] = current_node
                dfs_edges.append((current_node, neighbor))
                stack.append((neighbor, current_level + 1))

    return dfs_edges, level

# Add Random Order traversal function
def random_order_tree(G, start_node):
    """Traverse nodes in random order and create a random tree as list of edges and levels."""
    nodes = list(G.nodes())
    random.shuffle(nodes)  # Randomize node order
    visited = set()
    random_edges = []
    levels = {}
    parent = {start_node: None}
    levels[start_node] = 0
    queue = deque([(start_node, 0)])

    while queue:
        current_node, level = queue.popleft()
        visited.add(current_node)

        for neighbor in nodes:
            if neighbor not in visited and neighbor != current_node:
                visited.add(neighbor)
                random_edges.append((current_node, neighbor))
                queue.append((neighbor, level + 1))
                levels[neighbor] = level + 1

    return random_edges, levels

def dijkstra_tree(G, start_node):
    """Perform Dijkstra's algorithm and return the shortest path tree as a list of edges and distances."""
    length, path = nx.single_source_dijkstra(G, start_node, weight='weight')
    dijkstra_edges = []
    for target_node in path:
        if target_node != start_node:
            path_nodes = path[target_node]
            edges_in_path = list(zip(path_nodes[:-1], path_nodes[1:]))
            dijkstra_edges.extend(edges_in_path)
    # Remove duplicates
    dijkstra_edges = list(set(dijkstra_edges))
    return dijkstra_edges, length

def dijkstra_tree_explicit(G, start_node):
    """Perform Dijkstra's algorithm explicitly and return the shortest path tree as a list of edges and distances."""
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_node] = 0
    previous_nodes = {}
    visited = set()
    heap = [(0, start_node)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor in G.neighbors(current_node):
            edge_weight = G.edges[current_node, neighbor]['weight']
            distance = current_distance + edge_weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(heap, (distance, neighbor))

    # Build the shortest path tree
    dijkstra_edges = []
    for node in distances:
        if node != start_node and node in previous_nodes:
            dijkstra_edges.append((previous_nodes[node], node))

    return dijkstra_edges, distances

def astar_search(G, start_node, target_node):
    """Perform A* search from start_node to target_node."""
    path = nx.astar_path(G, start_node, target_node, weight='weight')
    astar_edges = list(zip(path[:-1], path[1:]))
    return astar_edges

def linear_gradient(start_color, end_color, steps):
    """Generate a list of colors forming a linear gradient between start and end colors."""
    gradient = []
    for i in range(steps):
        interpolated = [
            int(start_color[j] + (float(i) / (steps - 1)) * (end_color[j] - start_color[j]))
            for j in range(3)
        ]
        gradient.append(tuple(interpolated))
    return gradient

def draw_tree_with_gradient(image, G, tree_edges, node_values, line_width=4, start_color=(255, 255, 0), end_color=(128, 128, 0)):
    """Draw a tree on the image using a color gradient based on node values."""
    draw = ImageDraw.Draw(image)
    max_value = max(node_values.values())
    min_value = min(node_values.values())
    num_colors = 256  # Number of colors in the gradient
    gradient = linear_gradient(start_color, end_color, num_colors)
    for u, v in tree_edges:
        x1, y1 = G.nodes[u]['position']
        x2, y2 = G.nodes[v]['position']
        # Normalize node value to select color
        value = node_values[v]
        normalized_value = (value - min_value) / (max_value - min_value + 1e-6)
        color_index = int(normalized_value * (num_colors - 1))
        line_color = gradient[color_index]
        draw.line([x1, y1, x2, y2], fill=line_color, width=line_width)
    return image

def draw_astar_path(image, G, astar_edges, line_width=4):
    """Draw the A* path on the image using magenta color."""
    draw = ImageDraw.Draw(image)
    # Use magenta color for A* path
    line_color = (255, 0, 255)
    for u, v in astar_edges:
        x1, y1 = G.nodes[u]['position']
        x2, y2 = G.nodes[v]['position']
        draw.line([x1, y1, x2, y2], fill=line_color, width=line_width)
    return image

def highlight_node(image, G, node, color=(255, 0, 0), diameter=5):
    """Highlight a node by overlaying it last."""
    draw = ImageDraw.Draw(image)
    x, y = G.nodes[node]['position']
    radius = diameter // 2
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bbox, fill=color)
    return image

# Update process_image function to include DFS and Random Order trees
def process_image(image_path, Xstep=33, Ystep=33, line_width=4, bbox_size=1,
                  bfs_start_color=(255, 255, 0), bfs_end_color=(50, 50, 0),
                  dfs_start_color=(0, 255, 0), dfs_end_color=(0, 100, 0),
                  random_start_color=(0, 0, 255), random_end_color=(0, 0, 100),
                  djkstra_start_color=(255, 255, 255), djkstra_end_color=(128, 128, 128),
                  astar_color=(255, 0, 255)):

    random.seed(1)
    # Load image and setup as before
    rgb_array, image_size, original_image = load_image(image_path)
    nodes = sample_pixels(rgb_array, Xstep=Xstep, Ystep=Ystep)
    G = create_graph(nodes, Xstep=Xstep, Ystep=Ystep)
    G = calculate_edge_weights(G, rgb_array)
    source_node = random.choice(list(G.nodes()))

    # --- BFS Analysis ---
    bfs_edges, levels = bfs_tree(G, source_node)
    image_bfs = original_image.copy()
    image_bfs = draw_graph(G, image_bfs, bbox_size=bbox_size)
    image_bfs = draw_tree_with_gradient(image_bfs, G, bfs_edges, levels, line_width=line_width,
                                        start_color=bfs_start_color, end_color=bfs_end_color)
    image_bfs = highlight_node(image_bfs, G, source_node, color=(255, 0, 0), diameter=5)
    image_bfs.save(f'{os.path.splitext(image_path)[0]}_graph_bfs.png')

    # --- DFS Analysis ---
    dfs_edges, levels_dfs = dfs_tree(G, source_node)
    image_dfs = original_image.copy()
    image_dfs = draw_graph(G, image_dfs, bbox_size=bbox_size)
    image_dfs = draw_tree_with_gradient(image_dfs, G, dfs_edges, levels_dfs, line_width=line_width,
                                        start_color=dfs_start_color, end_color=dfs_end_color)
    image_dfs = highlight_node(image_dfs, G, source_node, color=(255, 0, 0), diameter=5)
    image_dfs.save(f'{os.path.splitext(image_path)[0]}_graph_dfs.png')

    # --- Random Order Analysis ---
    random_edges, levels_random = random_order_tree(G, source_node)
    image_random = original_image.copy()
    image_random = draw_graph(G, image_random, bbox_size=bbox_size)
    image_random = draw_tree_with_gradient(image_random, G, random_edges, levels_random, line_width=line_width,
                                           start_color=random_start_color, end_color=random_end_color)
    image_random = highlight_node(image_random, G, source_node, color=(255, 0, 0), diameter=5)
    image_random.save(f'{os.path.splitext(image_path)[0]}_graph_random.png')

    # --- Dijkstra's Algorithm ---
    dijkstra_edges, distances = dijkstra_tree(G, source_node)
    image_dijkstra = original_image.copy()
    image_dijkstra = draw_graph(G, image_dijkstra, bbox_size=bbox_size)
    image_dijkstra = draw_tree_with_gradient(image_dijkstra, G, dijkstra_edges, distances, line_width=line_width,
                                             start_color=djkstra_start_color, end_color=djkstra_end_color)
    image_dijkstra = highlight_node(image_dijkstra, G, source_node, color=(255, 0, 0), diameter=5)
    image_dijkstra.save(f'{os.path.splitext(image_path)[0]}_graph_dijkstra.png')
    print(f"Images saved for BFS, DFS, Random Order, and Dijkstra trees.")


    # --- A* Search ---
    target_node = random.choice(list(G.nodes()))
    astar_edges = astar_search(G, source_node, target_node)
    image_astar = original_image.copy()
    image_astar = draw_graph(G, image_astar, bbox_size=bbox_size)
    image_astar = draw_astar_path(image_astar, G, astar_edges, line_width=line_width)
    image_astar = highlight_node(image_astar, G, source_node, astar_color, diameter=5)
    image_astar = highlight_node(image_astar, G, target_node, astar_color, diameter=5)
    image_astar.save(f'{os.path.splitext(image_path)[0]}_graph_astar.png')
    print(f"Image saved for A* search path.")

image_paths = glob.glob('../images/mapWhite.png')

def main():
    import glob

    image_paths = glob.glob('../images/mapYellow.jpg')
    for image_path in image_paths:
        process_image(
            image_path,
            Xstep=20,
            Ystep=20,
            line_width=4,
            bbox_size=1,
            bfs_start_color=(255, 255, 0),
            bfs_end_color=(100, 100, 0),
            dfs_start_color=(0, 255, 0),
            dfs_end_color=(0, 100, 0),
            random_start_color=(0, 0, 255),
            random_end_color=(0, 0, 100),
            djkstra_start_color=(255, 255, 255),
            djkstra_end_color=(128, 128, 128),
            astar_color=(255, 0, 255)
        )

    image_paths = glob.glob('../images/mapWhite.png')
    for image_path in image_paths:
        process_image(
            image_path,
            Xstep=20,
            Ystep=20,
            line_width=4,
            bbox_size=1,
            bfs_start_color=(0, 0, 0),
            bfs_end_color=(0, 0, 0),
            dfs_start_color=(0, 0, 0),
            dfs_end_color=(0, 0, 0),
            random_start_color=(0, 0, 0),
            random_end_color=(0, 0, 0),
            djkstra_start_color=(0, 150, 150),
            djkstra_end_color=(0, 0, 0),
            astar_color=(0, 255, 255)
        )

if __name__ == '__main__':
    main()