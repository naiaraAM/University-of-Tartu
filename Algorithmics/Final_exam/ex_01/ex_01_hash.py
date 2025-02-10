import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from concurrent.futures import ProcessPoolExecutor
from hashlib import md5
from scipy.spatial.distance import cdist

def image_to_matrix(image_path, target_size):
    image = Image.open(image_path).convert('RGB')
    image = image.resize(target_size, Image.LANCZOS)
    return np.array(image, dtype=np.float32)

def extract_vertical_lines(image_rgb):
    return np.moveaxis(image_rgb, 1, 0)

def normalize_vectors(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return vectors / norms

def compute_hash_for_block(block):
    block_bytes = block.tobytes()
    return int(md5(block_bytes).hexdigest(), 16)

def process_image_blocks(image, n):
    blocks = []
    max_lines = image.shape[0]
    for k in range(0, max_lines - n + 1, n):
        block = image[k:k + n]
        block_hash = compute_hash_for_block(block)
        blocks.append((k, k + n, block_hash))
    return blocks

def compare_blocks(blocks1, blocks2, i, j, hash_range):
    similar_blocks = []
    for (k1_start, k1_end, hash1) in blocks1:
        for (k2_start, k2_end, hash2) in blocks2:
            if i == j and k1_start == k2_start:
                continue
            if abs(hash1 - hash2) <= hash_range:
                similar_blocks.append((i, j, k1_start, k1_end, k2_start, k2_end))
    return similar_blocks

def compute_cosine_similarities_batch(norm_lines1, norm_lines2):
    if norm_lines1.shape[1] != norm_lines2.shape[1]:
        raise ValueError("norm_lines1 and norm_lines2 must have the same number of columns")
    return 1 - cdist(norm_lines1, norm_lines2, 'cosine')

def process_image_pairs(args):
    i, j, norm_lines_i, norm_lines_j, similar_blocks, n = args
    similarities = []
    for (k1_start, k1_end, k2_start, k2_end) in similar_blocks:
        segment_similarity = compute_cosine_similarities_batch(
            norm_lines_i[k1_start:k1_end],
            norm_lines_j[k2_start:k2_end]
        ).mean()
        similarities.append((i, j, (k1_start, k1_end), (k2_start, k2_end), segment_similarity))
    return similarities

def visualize_similar_lines(image1, image2, range1, range2, similarity, n, img1_name, img2_name):
    cropped_image1 = image1[:, range1[0]:range1[0] + n, :]
    cropped_image2 = image2[:, range2[0]:range2[0] + n, :]

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    ax0 = plt.subplot(gs[0])
    ax0.imshow(cropped_image1 / 255.0)
    ax0.set_title(f"{img1_name} - Lines {range1[0]}-{range1[0] + n - 1}")
    ax0.axis('off')

    ax1 = plt.subplot(gs[1])
    ax1.imshow(cropped_image2 / 255.0)
    ax1.set_title(f"{img2_name} - Lines {range2[0]}-{range2[0] + n - 1}")
    ax1.axis('off')

    plt.suptitle(f"Similarity: {similarity:.4f}", fontsize=16)
    plt.tight_layout()
    plt.show()

def main(n):
    target_size = (256, 256)
    hash_range = 5000**5000
    list_images = os.listdir('img')
    matrix_images = [image_to_matrix(os.path.join('img', img), target_size) for img in list_images]
    vertical_lines = [extract_vertical_lines(img) for img in matrix_images]
    normalized_lines = [normalize_vectors(lines.reshape(lines.shape[0], -1)) for lines in vertical_lines]

    num_features = normalized_lines[0].shape[1]
    for lines in normalized_lines:
        if lines.shape[1] != num_features:
            raise ValueError("All images must have the same number of features after normalization")

    image_blocks = [process_image_blocks(lines, n) for lines in normalized_lines]

    similar_blocks = []
    for i in range(len(image_blocks)):
        for j in range(i, len(image_blocks)):
            similar_blocks.extend(compare_blocks(image_blocks[i], image_blocks[j], i, j, hash_range))

    tasks = []
    for (i, j, k1_start, k1_end, k2_start, k2_end) in similar_blocks:
        tasks.append((i, j, normalized_lines[i], normalized_lines[j], [(k1_start, k1_end, k2_start, k2_end)], n))

    num_cores = os.cpu_count()
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = executor.map(process_image_pairs, tasks)

    index_similarities = [item for sublist in results for item in sublist]
    index_similarities.sort(key=lambda x: x[4], reverse=True)

    print("Most similar vertical line groups:")
    for idx in range(min(10, len(index_similarities))):
        img1_idx, img2_idx, range1, range2, similarity = index_similarities[idx]
        print(f"Image {list_images[img1_idx]} and Image {list_images[img2_idx]}")
        print(f"Vertical lines {range1[0]}-{range1[1] - 1} and {range2[0]}-{range2[1] - 1}")
        print(f"Cosine similarity: {similarity:.4f}")
        print()

        visualize_similar_lines(
            matrix_images[img1_idx],
            matrix_images[img2_idx],
            range1,
            range2,
            similarity,
            n,
            list_images[img1_idx],
            list_images[img2_idx]
        )
    return index_similarities

if __name__ == '__main__':
    main(1)