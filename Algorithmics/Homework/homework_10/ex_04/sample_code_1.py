from PIL import Image
import os
import random

def shuffle_indices(rows):
    indices = list(range(rows))
    random.shuffle(indices)
    return indices

def modify_image_rows(image, indices):
    rgb_matrix = list(image.getdata())
    width, height = image.size
    modified_rgb = [rgb_matrix[i * width:(i + 1) * width] for i in indices]
    new_img = Image.new('RGB', (width, height))
    new_img.putdata([pixel for row in modified_rgb for pixel in row])
    return new_img

def process_images(folder_path):
    extensions = ('.jpg', '.jpeg', '.webp', '.png')
    for entry in os.listdir(folder_path):
        if entry.lower().endswith(extensions) and '_shuffled' not in entry and '_sorted' not in entry:
            file_path = os.path.join(folder_path, entry)
            with Image.open(file_path) as img:
                image = img.convert('RGB')
                # Shuffled version
                shuffled_indices = shuffle_indices(image.height)
                shuffled_image = modify_image_rows(image, shuffled_indices)
                shuffled_image.save(os.path.join(folder_path, f'{os.path.splitext(entry)[0]}_shuffled.png'))

def process_images_in_cwd():
    cwd = os.getcwd()  # Get the current working directory
    process_images(cwd)  # Process all image files in the current directory

# Call the function to process images in the current working directory
process_images_in_cwd()
