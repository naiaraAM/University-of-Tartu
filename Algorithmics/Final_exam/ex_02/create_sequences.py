import random

def generate_sequences(num_samples, length):
    options = ['abc', 'ab']
    sequences = []

    for _ in range(num_samples):
        sequence = ''
        while len(sequence) < length:
            sequence += random.choice(options)
        sequences.append(sequence[:length])

    return sequences

num_samples = 1
length = [2, 3, 8, 13, 21, 25, 34, 44, 55, 89]
for l in length:
    print(f'Sequences of length {l}: {generate_sequences(num_samples, l)}')
    print(generate_sequences(num_samples, l))