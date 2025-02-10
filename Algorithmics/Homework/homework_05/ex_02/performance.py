import time
import numpy as np
from sklearn.neighbors import KDTree
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
from PIL import Image
import random
import os
import matplotlib.pyplot as plt

# Function to load image from a local file
def load_image(input_path):
    if os.path.isfile(input_path):
        try:
            img = Image.open(input_path)
            return img
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    return None

# Function to extract blocks and their positions from an image
def extract_blocks_with_positions(image_array, block_size):
    block_height, block_width = block_size
    img_height, img_width, channels = image_array.shape

    # Calculate number of blocks
    num_blocks_vertical = img_height // block_height
    num_blocks_horizontal = img_width // block_width

    trimmed_height = num_blocks_vertical * block_height
    trimmed_width = num_blocks_horizontal * block_width
    trimmed_image = image_array[:trimmed_height, :trimmed_width, :]

    blocks = []
    positions = []

    for i in range(0, trimmed_height, block_height):
        for j in range(0, trimmed_width, block_width):
            block = trimmed_image[i:i+block_height, j:j+block_width, :]
            blocks.append(block.flatten())
            positions.append((j, i))

    blocks = np.array(blocks)
    positions = np.array(positions)

    return blocks, positions

# Function to perform brute-force k-NN search using Euclidean distance
def brute_force_knn(blocks_transformed, query_vector, k):
    distances = euclidean_distances(query_vector.reshape(1, -1), blocks_transformed).flatten()
    nearest_indices = np.argsort(distances)[:k]
    return nearest_indices, distances[nearest_indices]

# Function to perform k-NN search using KD-Tree
def kd_tree_knn(tree, query_vector, k):
    dist, ind = tree.query(query_vector.reshape(1, -1), k=k)
    return ind.flatten(), dist.flatten()

# Timing comparison between brute-force and KD-Tree
def compare_knn_methods(blocks, block_size, k=10):
    # Perform PCA on the blocks to reduce dimensionality
    blocks_float = blocks.astype(float)
    pca = PCA(n_components=2)
    blocks_pca = pca.fit_transform(blocks_float)

    # Create a KD-Tree from the PCA-transformed blocks
    kd_tree = KDTree(blocks_pca)

    # Select random query point
    random_index = random.randint(0, len(blocks) - 1)
    query_vector = blocks_pca[random_index]

    # Brute-force k-NN search
    start_time = time.time()
    bf_indices, bf_distances = brute_force_knn(blocks_pca, query_vector, k)
    brute_force_time = time.time() - start_time

    # KD-Tree k-NN search
    start_time = time.time()
    kd_indices, kd_distances = kd_tree_knn(kd_tree, query_vector, k)
    kd_tree_time = time.time() - start_time

    # Print comparison
    print(f"\nBlock size {block_size}")
    print(f"Brute-force time: {brute_force_time:.6f} seconds")
    print(f"KD-Tree time: {kd_tree_time:.6f} seconds")

    return brute_force_time, kd_tree_time

# Main code to load image, extract blocks, and compare methods
input_path = '../images/colors.jpeg'  # Replace with the actual path to your image
img = load_image(input_path)

if img is not None:
    image_array = np.array(img)
    if image_array.shape[2] == 4:
        image_array = image_array[:, :, :3]  # Remove alpha channel if present
    height, width, channels = image_array.shape

    block_sizes = [
                   (1, 101), (1, 102), (1, 103), (1, 104), (1, 105), (1, 106), (1, 107), (1, 108), (1, 109), (1, 110),
                   (1, 111), (1, 112), (1, 113), (1, 114), (1, 115), (1, 116), (1, 117), (1, 118), (1, 119), (1, 120),
                   (1, 121), (1, 122), (1, 123), (1, 124), (1, 125), (1, 126), (1, 127), (1, 128), (1, 129), (1, 130),
                   (1, 131), (1, 132), (1, 133), (1, 134), (1, 135), (1, 136), (1, 137), (1, 138), (1, 139), (1, 140),
                   (1, 141), (1, 142), (1, 143), (1, 144), (1, 145), (1, 146), (1, 147), (1, 148), (1, 149), (1, 150),
                   (1, 151), (1, 152), (1, 153), (1, 154), (1, 155), (1, 156), (1, 157), (1, 158), (1, 159), (1, 160),
                   (1, 161), (1, 162), (1, 163), (1, 164), (1, 165), (1, 166), (1, 167), (1, 168), (1, 169), (1, 170),
                   (1, 171), (1, 172), (1, 173), (1, 174), (1, 175), (1, 176), (1, 177), (1, 178), (1, 179), (1, 180),
                   (1, 181), (1, 182), (1, 183), (1, 184), (1, 185), (1, 186), (1, 187), (1, 188), (1, 189), (1, 190),
                   (1, 191), (1, 192), (1, 193), (1, 194), (1, 195), (1, 196), (1, 197), (1, 198), (1, 199), (1, 200),]
    brute_force_times = []
    kd_tree_times = []

    for block_size in block_sizes:
        print(f"\nProcessing block size: {block_size}")
        blocks, positions = extract_blocks_with_positions(image_array, block_size)
        num_blocks = blocks.shape[0]
        vector_dim = blocks.shape[1]

        print(f"Total blocks: {num_blocks}, Vector dimension: {vector_dim}")

        # Compare performance of brute-force and KD-Tree
        bf_time, kd_time = compare_knn_methods(blocks, block_size)
        brute_force_times.append(bf_time)
        kd_tree_times.append(kd_time)

    # Plotting the performance comparison line plot
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(block_sizes)), brute_force_times, label='Brute-force')
    plt.plot(range(len(block_sizes)), kd_tree_times, label='KD-Tree')
    plt.xticks(range(len(block_sizes)), [f"{size[0]}x{size[1]}" for size in block_sizes], rotation=45)
    plt.xlabel('Block Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison of KD-Tree')
    plt.legend()
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.show()

else:
    print("Image could not be loaded. Please check the file path.")
