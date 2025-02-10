import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np


# Generate a repeating pattern that causes KMP's worst-case behavior
def generate_kmp_worst_case_pattern(length):
    return "a" * (length - 1) + "b"


# Generate a text that contains the worst-case pattern repeatedly
def generate_text(length, pattern):
    repeat_count = length // len(pattern)
    remaining_chars = length % len(pattern)
    return pattern * repeat_count + pattern[:remaining_chars]


# Compute the prefix function for KMP
def compute_prefix_function(pattern):
    m = len(pattern)
    prefix = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = prefix[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        prefix[i] = j
    return prefix


# KMP Pattern Matching
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    prefix = compute_prefix_function(pattern)
    matches = []
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = prefix[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            matches.append(i - m + 1)
            j = prefix[j - 1]
    return matches


# Parameters
text_length = 100000
pattern_lengths = [5, 10, 50, 100, 200, 500, 1000]

# Run tests for KMP
times = []
for pattern_length in pattern_lengths:
    pattern = generate_kmp_worst_case_pattern(pattern_length)
    text = generate_text(text_length, pattern)

    start_time = time.time()
    kmp_search(text, pattern)
    elapsed_time = time.time() - start_time

    times.append(elapsed_time)

# Visualization
plt.figure(figsize=(10, 6))
plt.plot(pattern_lengths, times, marker='o', linestyle='-', color='blue')
plt.title('KMP Worst-Case Execution Time')
plt.xlabel('Pattern Length')
plt.ylabel('Time Taken (seconds)')
plt.grid(True)
plt.show()
