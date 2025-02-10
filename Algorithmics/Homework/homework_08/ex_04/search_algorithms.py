import heapq
import os
import random
from PIL import Image, ImageDraw
import numpy as np

from Homework.homework_08.ex_03.images_code import load_image, sample_pixels, create_graph, calculate_edge_weights, \
    draw_graph, highlight_node


def explicit_dijkstra(G, start_node):
    """Perform Dijkstra's algorithm explicitly and return the shortest path tree as a list of edges and distances."""
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_node] = 0
    previous_nodes = {}
    visited = set()
    heap = [(0, start_node)]
    search_front = []

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        search_front.append(current_node)

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

    return dijkstra_edges, distances, search_front

def explicit_astar(G, start_node, target_node):
    """Perform A* search explicitly and return the shortest path tree as a list of edges and distances."""
    def heuristic(node1, node2):
        x1, y1 = G.nodes[node1]['position']
        x2, y2 = G.nodes[node2]['position']
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    distances = {node: float('inf') for node in G.nodes()}
    distances[start_node] = 0
    previous_nodes = {}
    visited = set()
    heap = [(0, start_node)]
    search_front = []

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)
        search_front.append(current_node)

        if current_node == target_node:
            break

        for neighbor in G.neighbors(current_node):
            edge_weight = G.edges[current_node, neighbor]['weight']
            distance = current_distance + edge_weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                priority = distance + heuristic(neighbor, target_node)
                previous_nodes[neighbor] = current_node
                heapq.heappush(heap, (priority, neighbor))

    # Build the shortest path tree
    astar_edges = []
    for node in distances:
        if node != start_node and node in previous_nodes:
            astar_edges.append((previous_nodes[node], node))

    return astar_edges, distances, search_front


def visualize_search_front(image, G, search_front, step, base_color=(0, 255, 0), diameter=10):
    """Visualize the search front on the image with a gradient color."""
    draw = ImageDraw.Draw(image)
    max_intensity = 255
    for i, node in enumerate(search_front):
        if i % step == 0:
            x, y = G.nodes[node]['position']
            radius = diameter // 2
            bbox = [x - radius, y - radius, x + radius, y + radius]

            # Calculate intensity based on the position in the search front
            intensity = int(max_intensity * (1 - i / len(search_front)))
            color = tuple(int(c * intensity / max_intensity) for c in base_color)

            draw.ellipse(bbox, fill=color)
    return image

# python
def process_image_with_search(image_path, Xstep=33, Ystep=33, line_width=4, bbox_size=1,
                              search_step=20, dijkstra_color=(0, 255, 0), astar_color=(0, 255, 0)):
    random.seed(1)
    # Load image and setup as before
    rgb_array, image_size, original_image = load_image(image_path)
    nodes = sample_pixels(rgb_array, Xstep=Xstep, Ystep=Ystep)
    G = create_graph(nodes, Xstep=Xstep, Ystep=Ystep)
    G = calculate_edge_weights(G, rgb_array)
    source_node = random.choice(list(G.nodes()))
    target_node = random.choice(list(G.nodes()))

    # --- Dijkstra's Algorithm ---
    dijkstra_edges, distances, dijkstra_front = explicit_dijkstra(G, source_node)
    image_dijkstra = original_image.copy()
    image_dijkstra = draw_graph(G, image_dijkstra, bbox_size=bbox_size)
    image_dijkstra = visualize_search_front(image_dijkstra, G, dijkstra_front, search_step, base_color=dijkstra_color)
    image_dijkstra = highlight_node(image_dijkstra, G, source_node, color=(255, 0, 0), diameter=5)
    image_dijkstra = highlight_node(image_dijkstra, G, target_node, color=(255, 255, 0), diameter=5)  # Bright color for target node
    image_dijkstra.save(f'{os.path.splitext(image_path)[0]}_dijkstra_front.png')

    # --- A* Search ---
    astar_edges, distances, astar_front = explicit_astar(G, source_node, target_node)
    image_astar = original_image.copy()
    image_astar = draw_graph(G, image_astar, bbox_size=bbox_size)
    image_astar = visualize_search_front(image_astar, G, astar_front, search_step, base_color=astar_color)
    image_astar = highlight_node(image_astar, G, source_node, color=(255, 0, 0), diameter=5)
    image_astar = highlight_node(image_astar, G, target_node, color=(255, 255, 0), diameter=5)  # Bright color for target node
    image_astar.save(f'{os.path.splitext(image_path)[0]}_astar_front.png')

    print(f"Images saved for Dijkstra and A* search fronts.")

if __name__ == '__main__':
    import glob
    image_paths = glob.glob('../images/mapYellow.jpg')
    for image_path in image_paths:
        process_image_with_search(image_path, Xstep=20, Ystep=20, line_width=4, bbox_size=1, search_step=20)