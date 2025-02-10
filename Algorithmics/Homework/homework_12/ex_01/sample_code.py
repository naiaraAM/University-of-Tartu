import time
import random
import string
import numpy as np
from tabulate import tabulate

# Generate random strings of specified sizes using specific alphabet sizes
def generate_strings(sizes, alphabet_sizes):
    alphabet_base = string.ascii_letters + string.digits
    results = {}
    for size in sizes:
        for alpha_size in alphabet_sizes:
            alphabet = random.sample(alphabet_base, alpha_size)  # Ensure unique characters
            results[(size, alpha_size)] = ''.join(random.choices(alphabet, k=size))
    return results

# Naive search function
def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    occurrences = []
    for start in range(n - m + 1):
        match = True
        for j in range(m):
            if text[start + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(start)
    return occurrences

# KMP search function
def kmp_search(text, pattern):
    # Preprocess pattern to create the longest prefix suffix table
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    # Perform the KMP search
    n = len(text)
    m = len(pattern)
    i = 0
    j = 0
    occurrences = []
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            occurrences.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return occurrences

def boyer_moore_search(text, pattern):
    # Function to create the bad character table:
    def build_bad_character_table(pattern):
        # Initialize bad character table with default shift values set to the pattern's length
        bad_char = {char: -1 for char in set(text)}  # Cover all text characters
        for index, char in enumerate(pattern):
            bad_char[char] = index  # Set index of character's last occurrence in pattern
        return bad_char

    # Preprocess the pattern to create the bad character table:
    bad_char = build_bad_character_table(pattern)
    m = len(pattern)
    n = len(text)
    occurrences = []

    # Start searching:
    s = 0  # s is the shift of the pattern with respect to the text
    while s <= n - m:
        j = m - 1

        # Reduce j while characters of pattern and text are matching at this shift s
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # If the pattern is present at the current shift, then index j will become -1
        if j < 0:
            occurrences.append(s)
            # Shift the pattern so that the next character in text aligns with the last occurrence in the pattern
            s += (m - bad_char[text[s + m]] if (s + m < n) else 1)
        else:
            # Shift the pattern so that the bad character in text aligns with the last occurrence in pattern
            # Calculate the shift, ensuring not found characters shift the pattern length
            char_shift = m if bad_char.get(text[s + j]) == -1 else j - bad_char.get(text[s + j])
            s += max(1, char_shift)

    return occurrences

# Function to perform the testing of search algorithms
def test_search(algorithms, strings, pattern_lengths):
    summary_results = []

    for (size, alpha_size), text in strings.items():
        for plen in pattern_lengths:
            # Verify correctness with one pattern before measurement
            verification_pos = random.randint(0, len(text) - plen)
            verification_pattern = text[verification_pos:verification_pos + plen]
            for name, func in algorithms.items():
                verification_hits = func(text, verification_pattern)
                print(f'Verification for {name}, Size: {size}, Alphabet: {alpha_size}, Pattern Length: {plen}, Pattern: {verification_pattern}, First Hit: {verification_hits[0] if verification_hits else "No hit"}, Total Hits: {len(verification_hits)}')

            # Collect data for 11 trials per pattern, but skip timing the first trial
            for name, func in algorithms.items():
                times = []
                counts = []
                for trial in range(11):  # 11 runs, including the one to ignore
                    new_pos = random.randint(0, len(text) - plen)
                    new_pattern = text[new_pos:new_pos + plen]
                    start_time = time.time()
                    hits = func(text, new_pattern)
                    elapsed_time = (time.time() - start_time) * 1000
                    if trial != 0:
                        times.append(elapsed_time)
                        counts.append(len(hits))
                if times:
                    summary_results.append({
                        'Algorithm': name,
                        'String Size': size,
                        'Alphabet Size': alpha_size,
                        'Pattern Length': plen,
                        'Avg. Time (ms)': f"{np.mean(times):.6f}",
                        'Time StDev (ms)': f"{np.std(times):.6f}",
                        'Avg. Hits': f"{np.mean(counts):.6f}"
                    })

    return summary_results

# Configuration
alphabet_sizes = [2, 16, 50]
string_sizes = [100000]  # Adjusted to 100,000 as specified
pattern_lengths = [4, 16, 32 ]

# create a string that naive search will take a long time to find


strings = generate_strings(string_sizes, alphabet_sizes)
print(strings)
algorithms = {'Naive': naive_search, 'KMP': kmp_search, 'BM1': boyer_moore_search, 'Built-in': lambda t, p: [i for i in range(len(t)) if t.startswith(p, i)]}
# Execute and collect results
summary_results = test_search(algorithms, strings, pattern_lengths)

# Print summary results
print("\nSummary Results (10 Trials):")
print(tabulate(summary_results, headers="keys"))
