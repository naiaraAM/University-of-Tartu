import os
import csv
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter


def get_predominant_color(image):
    """Calculate the predominant color of an image."""
    np_image = np.array(image)
    pixels = np_image.reshape(-1, 3)
    counts = Counter(map(tuple, pixels))
    predominant_color = counts.most_common(1)[0][0]
    return predominant_color


def process_image(filename, directory, output_directory, size):
    """Resize the image and compute its predominant color."""
    try:
        img_path = os.path.join(directory, filename)
        if not os.path.isfile(img_path):
            raise FileNotFoundError(f"File {img_path} does not exist.")

        img = Image.open(img_path).convert("RGB")
        img = img.resize((size, size), Image.LANCZOS)
        img.save(os.path.join(output_directory, filename))
        predominant_color = get_predominant_color(img)
        return filename, predominant_color
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


def square_dataset_img(directory, output_directory, size, csv_file):
    """Create a dataset of squared images and their predominant colors."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    processed_files = set()
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            processed_files = {row[0] for row in reader}

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not processed_files:
            writer.writerow(['filename', 'r', 'g', 'b'])

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_image, filename, directory, output_directory, size)
                for filename in os.listdir(directory)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')) and filename not in processed_files
            ]

            for future in as_completed(futures):
                result = future.result()
                if result:
                    filename, predominant_color = result
                    writer.writerow([filename, *predominant_color])


def convert_image_to_pixel_art(path, filter_size):
    try:
        original_image = np.array(Image.open(path).convert("RGB"))
        height, width, _ = original_image.shape

        height = (height // filter_size) * filter_size
        width = (width // filter_size) * filter_size
        original_image = original_image[:height, :width, :]

        pixel_image = np.zeros((height // filter_size, width // filter_size, 3))

        for i in range(0, height, filter_size):
            for j in range(0, width, filter_size):
                block = original_image[i:i + filter_size, j:j + filter_size]
                pixel_image[i // filter_size, j // filter_size] = [
                    np.mean(block[:, :, 0]),
                    np.mean(block[:, :, 1]),
                    np.mean(block[:, :, 2])
                ]

        pixel_image = np.clip(pixel_image / 255.0, 0, 1)

        return pixel_image, (height // filter_size, width // filter_size)
    except Exception as e:
        print(f"Error in converting image to pixel art: {e}")
        return None, None


def search_closest_image_from(pixel_color):
    try:
        with open('predominant_colors.csv') as file:
            reader = csv.reader(file)
            next(reader)

            closest_image = None
            closest_distance = float('inf')

            for row in reader:
                filename, r, g, b = row
                color = np.array([float(r), float(g), float(b)]) / 255.0
                distance = np.linalg.norm(pixel_color - color)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_image = filename

        if closest_image:
            return Image.open(os.path.join('img_squared', closest_image)).convert("RGB")
    except Exception as e:
        print(f"Error in searching closest image: {e}")
    return None


def convert_to_collage(pixel_image, dimensions, filter_size):
    try:
        height, width = dimensions
        collage_height = height * filter_size
        collage_width = width * filter_size
        collage = Image.new("RGB", (collage_width, collage_height))

        for i in range(height):
            for j in range(width):
                closest_image = search_closest_image_from(pixel_image[i, j])
                if closest_image is not None:
                    closest_image = closest_image.resize((filter_size, filter_size), Image.LANCZOS)
                    collage.paste(closest_image, (j * filter_size, i * filter_size))

        return collage
    except Exception as e:
        print(f"Error in converting to collage: {e}")
        return None


if __name__ == '__main__':
    square_dataset_img('img_dataset', 'img_squared', 256, 'predominant_colors.csv')

    pixel_image, dimensions = convert_image_to_pixel_art('img_sample/fearless.jpg', 1)
    if pixel_image is not None and dimensions is not None:
        collage = convert_to_collage(pixel_image, dimensions, 1)
        if collage:
            collage.show()
