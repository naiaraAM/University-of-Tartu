# generate random text with the given paramentes

alphabet_size = 20
text_size = 20000000

import random
import string

def gen_text(alphabet_size, text_size):
    alphabet = string.ascii_letters[:alphabet_size]
    text = ''.join(random.choices(alphabet, k=text_size))
    return text

def save_to_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)


text = gen_text(alphabet_size, text_size)
save_to_file(text, 'random_text.txt')