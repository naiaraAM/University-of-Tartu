import random
import string
import time
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

random.seed(42)

def generate_text_with_pattern(length, alphabet_size, pattern):
    alphabet = string.ascii_lowercase[:alphabet_size - 1]  # Exclude last character to ensure no match
    text = ''.join(random.choice(alphabet) for _ in range(length - len(pattern)))
    text += pattern  # Append pattern to the end
    return text

def generate_pattern(length, alphabet_size):
    alphabet = string.ascii_lowercase[:alphabet_size]
    return ''.join(random.choice(alphabet) for _ in range(length))

def bm1_pattern_matching_worst_case(text, pattern):
    n = len(text)
    m = len(pattern)
    matches = []
    i = 0

    while i <= n - m:
        # Worst case: Every character causes a mismatch
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j == -1:
            matches.append(i)  # Pattern found
            i += m  # Jump the full length of the pattern
        else:
            i += max(1, j)  # Skip to the right position
    return matches

# Parameters
text_length = 100000
pattern_lengths = [5, 20, 50]
alphabet_sizes = [4, 8, 10, 20, 50]

patterns = []
for alph_size in alphabet_sizes:
    for pat_len in pattern_lengths:
        patterns.append(generate_pattern(pat_len, alph_size))

matches_bm1 = []
results_bm1 = []

# Run tests for Boyer-Moore in worst-case scenario
for alph_size in alphabet_sizes:
    for pat_len in pattern_lengths:
        pattern = generate_pattern(pat_len, alph_size)
        text = generate_text_with_pattern(text_length, alph_size, pattern)

        # BM1 pattern matching in worst-case scenario
        start_time = time.time()
        match_bm1 = bm1_pattern_matching_worst_case(text, pattern)
        end_time = time.time()
        elapsed_time_bm1 = end_time - start_time
        matches_bm1.append(match_bm1)

        last_match_bm1 = match_bm1[-1] if match_bm1 else None
        results_bm1.append([
            alph_size,
            len(pattern),
            len(match_bm1),
            last_match_bm1,
            elapsed_time_bm1,
        ])

headers = ["Alphabet size", "Pattern size", "Number of matches found", "Last match index", "Time taken"]
print("Boyer-Moore Algorithm (Worst Case) Results:")
print(tabulate(results_bm1, headers=headers, tablefmt="grid"))

# Visualization
fig, ax = plt.subplots(figsize=(12, 8))

# Prepare data for plotting
alphabet_sizes = sorted(set(result[0] for result in results_bm1))
pattern_sizes = sorted(set(result[1] for result in results_bm1))
times_taken_bm1 = {pat_size: [] for pat_size in pattern_sizes}

for alph_size in alphabet_sizes:
    for pat_size in pattern_sizes:
        for result in results_bm1:
            if result[0] == alph_size and result[1] == pat_size:
                times_taken_bm1[pat_size].append(result[4])

bar_width = 0.15
index = np.arange(len(alphabet_sizes))

for i, pat_size in enumerate(pattern_sizes):
    plt.bar(index + i * bar_width, times_taken_bm1[pat_size], bar_width, label=f'BM1 Worst Case - Pattern Size {pat_size}')

ax.set_xlabel('Alphabet Size')
ax.set_ylabel('Time Taken (s)')
ax.set_title('Time for Boyer-Moore Algorithm (Worst Case)')
ax.set_xticks(index + bar_width * (len(pattern_sizes) - 1) / 2)
ax.set_xticklabels(alphabet_sizes)
ax.legend()

plt.tight_layout()
plt.grid(True)
plt.show()
