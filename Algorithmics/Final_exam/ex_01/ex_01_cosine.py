import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from concurrent.futures import ProcessPoolExecutor

def image_to_matrix(image_path):
    image = Image.open(image_path).convert('RGB')
    return np.array(image, dtype=np.float32)

def extract_vertical_lines(image_rgb):
    return np.moveaxis(image_rgb, 1, 0)

def normalize_vectors(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return vectors / norms

def compute_cosine_similarities_batch(norm_lines1, norm_lines2):
    return np.dot(norm_lines1, norm_lines2.T)

def process_image_pairs(args):
    i, j, norm_lines_i, norm_lines_j, n = args
    similarities = []
    max_lines_i, max_lines_j = norm_lines_i.shape[0], norm_lines_j.shape[0]

    for k in range(0, max_lines_i - n + 1, n):
        for l in range(0, max_lines_j - n + 1, n):
            if i == j and k == l:
                continue

            segment_similarity = compute_cosine_similarities_batch(
                norm_lines_i[k:k + n],
                norm_lines_j[l:l + n]
            ).mean()

            similarities.append((i, j, (k, k + n), (l, l + n), segment_similarity))

    return similarities

def visualize_similar_lines(image1, image2, range1, range2, similarity, n):
    cropped_image1 = image1[:, range1[0]:range1[0] + n, :]
    cropped_image2 = image2[:, range2[0]:range2[0] + n, :]

    fig = plt.figure(figsize=(10, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

    ax0 = plt.subplot(gs[0])
    ax0.imshow(cropped_image1 / 255.0)
    ax0.set_title(f"Image 1 - Lines {range1[0]}-{range1[0] + n - 1}")
    ax0.axis('off')

    ax1 = plt.subplot(gs[1])
    ax1.imshow(cropped_image2 / 255.0)
    ax1.set_title(f"Image 2 - Lines {range2[0]}-{range2[0] + n - 1}")
    ax1.axis('off')

    plt.suptitle(f"Similarity: {similarity:.4f}", fontsize=16)
    plt.tight_layout()
    plt.show()

def main(n):
    list_images = os.listdir('img')
    matrix_images = [image_to_matrix(os.path.join('img', img)) for img in list_images]
    vertical_lines = [extract_vertical_lines(img) for img in matrix_images]
    normalized_lines = [normalize_vectors(lines.reshape(lines.shape[0], -1)) for lines in vertical_lines]

    tasks = []
    for i in range(len(normalized_lines)):
        for j in range(i, len(normalized_lines)):
            tasks.append((i, j, normalized_lines[i], normalized_lines[j], n))

    num_cores = os.cpu_count()
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        results = executor.map(process_image_pairs, tasks)

    index_similarities = [item for sublist in results for item in sublist]
    index_similarities.sort(key=lambda x: x[4], reverse=True)

    print("Most similar vertical line groups:")
    for idx in range(min(10, len(index_similarities))):
        img1_idx, img2_idx, range1, range2, similarity = index_similarities[idx]
        print(f"Image {img1_idx} and Image {img2_idx}")
        print(f"Vertical lines {range1[0]}-{range1[1] - 1} and {range2[0]}-{range2[1] - 1}")
        print(f"Cosine similarity: {similarity:.4f}")
        print()

        visualize_similar_lines(
            matrix_images[img1_idx],
            matrix_images[img2_idx],
            range1,
            range2,
            similarity,
            n
        )
        return index_similarities

if __name__ == '__main__':
    main(200)