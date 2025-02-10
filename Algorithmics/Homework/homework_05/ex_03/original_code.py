# Install necessary libraries (if not already installed)
# !pip install Pillow

# Import necessary libraries
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import random
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances, cosine_similarity
from urllib.parse import urlparse
import os

from Homework.homework_05.ex_03.random_proyection_tree import create_rp_tree, num_nodes

random.seed(0)  # Set random seed for reproducibility

# Function to load image from URL or local file
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

# Main code
# Provide the image path (either URL or local filename)
# input_path = 'https://digit.cs.ut.ee/~vilo/photos/52084941097_f27207539e_o.jpg'  # Example URL
input_path = '../images/colors.jpeg'  # Example local filename (ensure the file exists in your Colab environment)

# Load the image
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

    # Function to Extract Blocks and Positions
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

                block = trimmed_image[i:i+block_height, j:j+block_width, :]

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

    # Function to visualize PCA-transformed data
    def visualize_pca_data(blocks_pca, block_size):
        plt.figure(figsize=(8,6))
        plt.scatter(blocks_pca[:, 0], blocks_pca[:, 1], s=5, alpha=0.7)
        plt.title(f'PCA of Blocks (size={block_size})')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.show()

    # Function to perform K-NN search with different distance metrics
    def perform_knn_search(blocks_original, blocks_transformed, positions, random_indices, k=4):
        # For each selected vector
        for idx in random_indices:
            vector_original = blocks_original[idx].reshape(1, -1)
            vector_transformed = blocks_transformed[idx].reshape(1, -1)
            position = positions[idx]
            vector_contents = vector_original.flatten()
            vector_str = np.array2string(vector_contents, formatter={'int':lambda x: f'{x:3d}'}, separator=',', max_line_width=80)
            print(f"\nSelected Vector at Position X={position[0]:>4}, Y={position[1]:>4}    Vector: {vector_str}")

            # Compute distances in PCA-transformed space
            # Choose one of the following distance metrics:

            # Option 1: Euclidean distance using library function
            distances = euclidean_distances(vector_transformed, blocks_transformed).flatten()

            # Option 2: Euclidean distance using explicit function
            #distances = np.sqrt(np.sum((blocks_transformed - vector_transformed) ** 2, axis=1))

            # Option 3: Manhattan distance using library function
            # distances = manhattan_distances(vector_transformed, blocks_transformed).flatten()

            # Option 4: Manhattan distance using explicit function
            # distances = np.sum(np.abs(blocks_transformed - vector_transformed), axis=1)

            # Option 5: Cosine distance using library function
            # cosine_similarities = cosine_similarity(vector_transformed, blocks_transformed).flatten()
            # distances = 1 - cosine_similarities

            # Option 6: Cosine distance using explicit function
            # dot_products = np.sum(vector_transformed * blocks_transformed, axis=1)
            # norm_a = np.linalg.norm(vector_transformed)
            # norms_b = np.linalg.norm(blocks_transformed, axis=1)
            # cosine_similarities = dot_products / (norm_a * norms_b)
            # distances = 1 - cosine_similarities

            # Exclude self
            distances[idx] = np.inf

            # Find nearest neighbors
            nearest_indices = np.argsort(distances)[:k]

            print("Nearest neighbors in PCA-transformed space:")
            print(f"{'Index':>6}  {'X':>6}  {'Y':>6}  {'Distance':>12}    {'Vector Contents'}")
            for n_idx in nearest_indices:
                neighbor_vector = blocks_original[n_idx].flatten()
                neighbor_position = positions[n_idx]
                distance = distances[n_idx]
                neighbor_vector_str = np.array2string(neighbor_vector, formatter={'int':lambda x: f'{x:3d}'}, separator=',', max_line_width=80)
                print(f"{n_idx:>6}  {neighbor_position[0]:>6}  {neighbor_position[1]:>6}  {distance:12.4f}    {neighbor_vector_str}")

    # Step 3 and 4: Process Blocks and Perform Similarity Search
    block_sizes = [(1,1), (1,3), (3,4)]  # Block sizes to process

    for block_size in block_sizes:
        print(f"\nProcessing block size: {block_size}")
        blocks, positions = extract_blocks_with_positions(image_array, block_size)
        num_blocks = blocks.shape[0]
        vector_dim = blocks.shape[1]

        print(f"Total blocks: {num_blocks}, Vector dimension: {vector_dim}")

        # **No normalization; keep blocks as integer RGB values**

        # Apply PCA (convert to float for PCA computation)
        print("Applying PCA...")
        blocks_float = blocks.astype(float)  # Convert to float for PCA
        pca = PCA(n_components=2)
        blocks_pca = pca.fit_transform(blocks_float)

        _, num_nodes = create_rp_tree(blocks_pca)
        print(f"Total number of nodes in the RP-tree: {num_nodes}")

        # Visualize the PCA-transformed data
        visualize_pca_data(blocks_pca, block_size)



        # Select 5 random indices
        random_indices = random.sample(range(num_blocks), 5)

        # Perform K-NN search on PCA-transformed data
        print("Performing K-NN search on PCA-transformed data...")
        perform_knn_search(blocks, blocks_pca, positions, random_indices, k=10)

else:
    print("Image could not be loaded. Please check the input path or URL.")
