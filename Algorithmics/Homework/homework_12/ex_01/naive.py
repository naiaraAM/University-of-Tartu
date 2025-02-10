import random
import string
import time
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

random.seed(42)

def generate_text_with_pattern(length, alphabet_size, pattern):
    alphabet = string.ascii_lowercase[:alphabet_size - 1]
    text = ''.join(random.choice(alphabet) for _ in range(length - len(pattern)))
    text += pattern
    return text

def generate_pattern(length, alphabet_size):
    alphabet = string.ascii_lowercase[:alphabet_size]
    return ''.join(random.choice(alphabet) for _ in range(length))

def naive_pattern_matching(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)
    return matches

# Parameters
text_length = 100000
pattern_lengths = [5, 20, 50]
alphabet_sizes = [4, 8, 10, 20, 50]

patterns = []
for alph_size in alphabet_sizes:
    for pat_len in pattern_lengths:
        patterns.append(generate_pattern(pat_len, alph_size))

matches = []
results = []
for alph_size in alphabet_sizes:
    for pat_len in pattern_lengths:
        pattern = generate_pattern(pat_len, alph_size)
        text = generate_text_with_pattern(text_length, alph_size, pattern)
        start_time = time.time()
        match = naive_pattern_matching(text, pattern)
        end_time = time.time()
        matches.append(match)
        elapsed_time = end_time - start_time

        last_match = match[-1] if match else None
        results.append([
            alph_size,
            len(pattern),
            len(match),
            last_match,
            elapsed_time,
        ])

headers = ["Alphabet size", "Pattern size", "Number of matches found", "Last match index", "Time taken"]
print(tabulate(results, headers=headers, tablefmt="grid"))

# Visualization
fig, ax = plt.subplots(figsize=(12, 8))

# Prepare data for plotting
alphabet_sizes = sorted(set(result[0] for result in results))
pattern_sizes = sorted(set(result[1] for result in results))
times_taken = {pat_size: [] for pat_size in pattern_sizes}

for alph_size in alphabet_sizes:
    for pat_size in pattern_sizes:
        for result in results:
            if result[0] == alph_size and result[1] == pat_size:
                times_taken[pat_size].append(result[4])

bar_width = 0.15
index = np.arange(len(alphabet_sizes))

for i, pat_size in enumerate(pattern_sizes):
    plt.bar(index + i * bar_width, times_taken[pat_size], bar_width, label=f'Pattern Size {pat_size}')

ax.set_xlabel('Alphabet Size')
ax.set_ylabel('Time Taken (s)')
ax.set_title('Time Taken for Naive Pattern Matching')
ax.set_xticks(index + bar_width * (len(pattern_sizes) - 1) / 2)
ax.set_xticklabels(alphabet_sizes)
ax.legend()

plt.tight_layout()
plt.grid(True)
plt.show()