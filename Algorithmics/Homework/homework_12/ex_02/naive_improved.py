import random
import string
import time
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

from Homework.homework_12.ex_01.naive import naive_pattern_matching

random.seed(42)

def generate_text_with_pattern(length, alphabet_size, pattern):
    alphabet = string.ascii_lowercase[:alphabet_size - 1]
    text = ''.join(random.choice(alphabet) for _ in range(length - len(pattern)))
    text += pattern
    return text

def generate_pattern(length, alphabet_size):
    alphabet = string.ascii_lowercase[:alphabet_size]
    return ''.join(random.choice(alphabet) for _ in range(length))

def optimized_naive_pattern_matching(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    i = 0

    while i <= n - m:
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(i)
            i += m  # Skip the length of the pattern
        else:
            if text[i + m - 1] != pattern[-1]:
                i += m  # Skip the length of the pattern if the last character doesn't match
            else:
                i += 1  # Move to the next character in the text

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
        match_opt = optimized_naive_pattern_matching(text, pattern)
        end_time = time.time()
        matches.append(match_opt)
        elapsed_time_opt = end_time - start_time
        start_time = time.time()
        match_og = naive_pattern_matching(text, pattern)
        end_time = time.time()
        elapsed_time_og = end_time - start_time

        last_match = match_opt[-1] if match_opt else None
        results.append([
            alph_size,
            len(pattern),
            len(match_opt),
            last_match,
            elapsed_time_opt,
            elapsed_time_og,
        ])

headers = ["Alphabet size", "Pattern size", "Number of matches found", "Last match index", "Time taken (optimized)", "Time taken (Original)"]
print(tabulate(results, headers=headers, tablefmt="grid"))

# Visualization
fig, ax = plt.subplots(figsize=(14, 8))

# Prepare data for plotting
alphabet_sizes = sorted(set(result[0] for result in results))
pattern_sizes = sorted(set(result[1] for result in results))
times_taken_opt = {pat_size: [] for pat_size in pattern_sizes}
times_taken_og = {pat_size: [] for pat_size in pattern_sizes}

for alph_size in alphabet_sizes:
    for pat_size in pattern_sizes:
        for result in results:
            if result[0] == alph_size and result[1] == pat_size:
                times_taken_opt[pat_size].append(result[4])
                times_taken_og[pat_size].append(result[5])

# Plotting the line plot
for pat_size in pattern_sizes:
    plt.plot(alphabet_sizes, times_taken_opt[pat_size], marker='o', linestyle='-', label=f'Pattern Size {pat_size} (Optimized)')
    plt.plot(alphabet_sizes, times_taken_og[pat_size], marker='x', linestyle='--', label=f'Pattern Size {pat_size} (Original)')

ax.set_xlabel('Alphabet Size')
ax.set_ylabel('Time Taken (s)')
ax.set_title('Comparison of Optimized and Original Naive Pattern Matching')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()