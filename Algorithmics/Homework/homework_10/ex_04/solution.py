import numpy as np
from PIL import Image

def unshuffle_image(image_path, output_path):
    with Image.open(image_path) as img:
        rgb_matrix = list(img.getdata())
        width, height = img.size

        rows = [np.array(rgb_matrix[i * width:(i + 1) * width]) for i in range(height)]

        sorted_indices = []
        sorted_rows = []
        visited = set()
        current_index = 0
        sorted_indices.append(current_index)
        sorted_rows.append(rows[current_index])
        visited.add(current_index)

        while len(sorted_indices) < height:
            min_distance = float('inf')
            next_index = None
            for i in range(height):
                if i not in visited:
                    dist = np.linalg.norm(rows[current_index] - rows[i])
                    if dist < min_distance:
                        min_distance = dist
                        next_index = i

            sorted_indices.append(next_index)
            sorted_rows.append(rows[next_index])
            visited.add(next_index)
            current_index = next_index

        new_img = Image.new('RGB', (width, height))

        flattened_data = [tuple(pixel) for row in sorted_rows for pixel in row]
        new_img.putdata(flattened_data)

        new_img.save(output_path)
        return new_img


# Usage
unshuffle_image('hw_10_4_shuffled.png', 'hw10_4_ordered.png')
