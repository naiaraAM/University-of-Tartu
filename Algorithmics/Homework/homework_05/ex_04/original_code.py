import os
import random
from io import BytesIO
from urllib.parse import urlparse

import numpy as np
import requests
from PIL import UnidentifiedImageError, Image
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances
import time

random.seed(0)  # Set random seed for reproducibility

def extract_blocks_with_positions(image_array, block_size):
    block_height, block_width = block_size
    img_height, img_width, channels = image_array.shape

    # Calculate the number of blocks along height and width
    num_blocks_vertical = img_height // block_height
    num_blocks_horizontal = img_width // block_width

    # Trim the image to fit an integer number of blocks
    trimmed_height = num_blocks_vertical * block_height
    trimmed_width = num_blocks_horizontal * block_width
    trimmed_image = image_array[:trimmed_height, :trimmed_width, :]

    # Extract blocks and their positions
    blocks = []
    positions = []

    for i in range(0, trimmed_height, block_height):
        for j in range(0, trimmed_width, block_width):

            if random.random() > 0.5:  # Skip half of the blocks
                continue

            block = trimmed_image[i:i + block_height, j:j + block_width, :]

            # Check if block contains more than one pixel
            if block.size > 3:  # More than one pixel
                # Reshape block to (-1, 3), each row is an RGB triplet
                block_pixels = block.reshape(-1, 3)
                # Check if all RGB triplets are the same
                if np.all((block_pixels == block_pixels[0]).all(axis=1)):
                    # All pixels have the same RGB values
                    if random.random() > 0.1:  # Accept with 10% probability
                        continue  # Skip this block

            blocks.append(block.flatten())
            positions.append((j, i))  # (X, Y) position

    blocks = np.array(blocks)
    positions = np.array(positions)

    return blocks, positions

def load_image(input_path):
    if os.path.isfile(input_path):
        # Input is a local file
        try:
            img = Image.open(input_path)
            return img
        except UnidentifiedImageError:
            print(f"Could not identify image from the file: {input_path}")
            return None
    else:
        # Check if input is a URL
        parsed_url = urlparse(input_path)
        if parsed_url.scheme in ('http', 'https'):
            try:
                response = requests.get(input_path)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                return img
            except requests.exceptions.RequestException as e:
                print(f"Failed to retrieve image: {e}")
                return None
            except UnidentifiedImageError:
                print("Could not identify image from the URL.")
                return None
        else:
            print(f"The input '{input_path}' is neither a valid URL nor a local file.")
            return None

# Function to compare K-NN before and after PCA
def compare_knn_before_after_pca(blocks_original, positions, k=4, n_components=2):
    # Step 1: Perform K-NN on original data
    print("Performing K-NN on original high-dimensional data...")
    start_time = time.time()
    distances_original = euclidean_distances(blocks_original, blocks_original)
    neighbors_original = np.argsort(distances_original, axis=1)[:, 1:k+1]  # Exclude self (index 0)
    original_knn_time = time.time() - start_time
    print(f"Time for K-NN on original data: {original_knn_time:.4f} seconds")

    # Step 2: Apply PCA for dimensionality reduction
    print(f"Applying PCA to reduce dimensions to {n_components}...")
    pca = PCA(n_components=n_components)
    blocks_pca = pca.fit_transform(blocks_original)

    # Check how much variance is retained after PCA
    explained_variance = np.sum(pca.explained_variance_ratio_)
    print(f"Explained variance with {n_components} components: {explained_variance * 100:.2f}%")

    # Step 3: Perform K-NN on PCA-transformed data
    print("Performing K-NN on PCA-reduced data...")
    start_time = time.time()
    distances_pca = euclidean_distances(blocks_pca, blocks_pca)
    neighbors_pca = np.argsort(distances_pca, axis=1)[:, 1:k+1]
    pca_knn_time = time.time() - start_time
    print(f"Time for K-NN on PCA-reduced data: {pca_knn_time:.4f} seconds")

    # Step 4: Compare neighbors before and after PCA
    print("Comparing K-NN results before and after PCA...")
    total_blocks = blocks_original.shape[0]
    matching_neighbors = np.sum(neighbors_original == neighbors_pca)
    percentage_matching = (matching_neighbors / (total_blocks * k)) * 100
    print(f"Percentage of matching neighbors: {percentage_matching:.2f}%")

    # Return results
    return explained_variance, percentage_matching, original_knn_time, pca_knn_time

# Main code
# Load the image as already done in your original code
input_path = '../images/colors.jpeg'  # Provide your image path
img = load_image(input_path)

if img is not None:
    # Display the image
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis('off')
    plt.title('Original Image')
    plt.show()

    # Convert Image into RGB Matrix
    image_array = np.array(img)
    if image_array.shape[2] == 4:
        image_array = image_array[:, :, :3]  # Remove alpha channel if present
    height, width, channels = image_array.shape

    # Define block size for this test
    block_size = (3, 3)  # Example block size

    # Extract blocks and positions
    blocks, positions = extract_blocks_with_positions(image_array, block_size)
    print(f"Total blocks: {blocks.shape[0]}, Vector dimension: {blocks.shape[1]}")

    # Compare K-NN before and after PCA
    explained_variance, percentage_matching, original_knn_time, pca_knn_time = compare_knn_before_after_pca(blocks, positions, k=4, n_components=2)

    # Print final comparison results
    print("\n--- Final Comparison ---")
    print(f"Explained Variance (after PCA): {explained_variance * 100:.2f}%")
    print(f"Percentage of Matching Neighbors: {percentage_matching:.2f}%")
    print(f"K-NN Time (Original Data): {original_knn_time:.4f} seconds")
    print(f"K-NN Time (PCA Data): {pca_knn_time:.4f} seconds")

else:
    print("Image could not be loaded. Please check the input path or URL.")
