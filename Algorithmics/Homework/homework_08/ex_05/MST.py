import os
import random
from PIL import Image, ImageDraw
from Homework.homework_08.ex_03.images_code import load_image, sample_pixels, create_graph, calculate_edge_weights, draw_graph, highlight_node

def kruskal_mst(G):
    """Perform Kruskal's algorithm to find the Minimum Spanning Tree (MST)."""
    mst_edges = []
    parent = {node: node for node in G.nodes()}
    rank = {node: 0 for node in G.nodes()}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root1] = root2
                if rank[root1] == rank[root2]:
                    rank[root2] += 1

    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    for u, v, data in edges:
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v))

    return mst_edges

def visualize_mst(image, G, mst_edges, line_width=4, color=(0, 255, 0)):
    """Visualize the Minimum Spanning Tree (MST) on the image."""
    draw = ImageDraw.Draw(image)
    for u, v in mst_edges:
        x1, y1 = G.nodes[u]['position']
        x2, y2 = G.nodes[v]['position']
        draw.line([x1, y1, x2, y2], fill=color, width=line_width)
    return image

def process_image_with_mst(image_path, Xstep=33, Ystep=33, line_width=4, bbox_size=1, mst_color=(0, 255, 0)):
    random.seed(1)
    # Load image and setup as before
    rgb_array, image_size, original_image = load_image(image_path)
    nodes = sample_pixels(rgb_array, Xstep=Xstep, Ystep=Ystep)
    G = create_graph(nodes, Xstep=Xstep, Ystep=Ystep)
    G = calculate_edge_weights(G, rgb_array)
    source_node = random.choice(list(G.nodes()))

    # --- Kruskal's MST Algorithm ---
    mst_edges = kruskal_mst(G)
    image_mst = original_image.copy()
    image_mst = draw_graph(G, image_mst, bbox_size=bbox_size)
    image_mst = visualize_mst(image_mst, G, mst_edges, line_width=line_width, color=mst_color)
    image_mst = highlight_node(image_mst, G, source_node, color=(255, 0, 0), diameter=5)
    image_mst.save(f'{os.path.splitext(image_path)[0]}_mst.png')

    print(f"Image saved for MST.")

if __name__ == '__main__':
    import glob
    image_paths = glob.glob('../images/mapYellow.jpg')
    for image_path in image_paths:
        process_image_with_mst(image_path, Xstep=20, Ystep=20, line_width=4, bbox_size=1)