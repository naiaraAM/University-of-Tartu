import time
import numpy as np
from sklearn.neighbors import KDTree, BallTree
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
        for j in range(0, trimmed_width, block_width):  # FIX: Changed from j+j to j
            block = trimmed_image[i:i+block_height, j:j+block_width, :]
            blocks.append(block.flatten())
            positions.append((j, i))

    blocks = np.array(blocks)
    positions = np.array(positions)

    return blocks, positions


def kd_tree_knn(tree, query_vector, k):
    dist, ind = tree.query(query_vector.reshape(1, -1), k=k)
    return ind.flatten(), dist.flatten()

def ball_tree_knn(tree, query_vector, k):
    dist, ind = tree.query(query_vector.reshape(1, -1), k=k)
    return ind.flatten(), dist.flatten()

# Timing comparison between brute-force, KD-Tree, and Ball Tree
def compare_knn_methods(blocks, block_size, k=10):

    blocks_float = blocks.astype(float)
    pca = PCA(n_components=2)
    blocks_pca = pca.fit_transform(blocks_float)

    kd_tree = KDTree(blocks_pca)
    ball_tree = BallTree(blocks_pca)

    random_index = random.randint(0, len(blocks) - 1)
    query_vector = blocks_pca[random_index]

    start_time = time.time()
    kd_indices, kd_distances = kd_tree_knn(kd_tree, query_vector, k)
    kd_tree_time = time.time() - start_time

    start_time = time.time()
    bt_indices, bt_distances = ball_tree_knn(ball_tree, query_vector, k)
    ball_tree_time = time.time() - start_time

    # Print comparison
    print(f"\nBlock size {block_size}")
    print(f"KD-Tree time: {kd_tree_time:.6f} seconds")
    print(f"Ball Tree time: {ball_tree_time:.6f} seconds")

    return kd_tree_time, ball_tree_time

# Main code to load image, extract blocks, and compare methods
input_path = '../images/colors.jpeg'  # Replace with the actual path to your image
img = load_image(input_path)

if img is not None:
    image_array = np.array(img)
    if image_array.shape[2] == 4:
        image_array = image_array[:, :, :3]  # Remove alpha channel if present
    height, width, channels = image_array.shape

    block_sizes = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
                   (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20),
                   (1, 21 ), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30),]
    brute_force_times = []
    kd_tree_times = []
    ball_tree_times = []

    for block_size in block_sizes:
        print(f"\nProcessing block size: {block_size}")
        blocks, positions = extract_blocks_with_positions(image_array, block_size)
        num_blocks = blocks.shape[0]
        vector_dim = blocks.shape[1]

        print(f"Total blocks: {num_blocks}, Vector dimension: {vector_dim}")

        # Compare performance of KD-Tree, and Ball Tree
        kd_time, bt_time = compare_knn_methods(blocks, block_size)
        kd_tree_times.append(kd_time)
        ball_tree_times.append(bt_time)

    # Plotting the performance comparison line plot
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(block_sizes)), kd_tree_times, label='KD-Tree')
    plt.plot(range(len(block_sizes)), ball_tree_times, label='Ball Tree')
    plt.xticks(range(len(block_sizes)), [f"{size[0]}x{size[1]}" for size in block_sizes], rotation=45)
    plt.xlabel('Block Size')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison of KD-Tree, Ball Tree, and Brute-force K-NN')
    plt.legend()
    plt.tight_layout()
    plt.savefig('performance_comparison_indexing.png')
    plt.show()

else:
    print("Image could not be loaded. Please check the file path.")
