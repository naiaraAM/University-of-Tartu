import random
import time
from collections import deque
from Homework.homework_07.ex_03.word_gen import WordStreamGenerator

class NormalHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def insert(self, word):
        hashed_word = hash(word) % self.size
        if self.table[hashed_word] is None:
            self.table[hashed_word] = [[word, 1]]
        else:
            for pair in self.table[hashed_word]:
                if pair[0] == word:
                    pair[1] += 1
                    return
            self.table[hashed_word].append([word, 1])

    def get_all_items(self):
        items = []
        for bucket in self.table:
            if bucket is not None:
                items.extend(bucket)
        return items

    def sort(self):
        all_items = self.get_all_items()
        return sorted(all_items, key=lambda x: x[1], reverse=True)

class LogHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def insert(self, word):
        hashed_word = hash(word) % self.size
        if self.table[hashed_word] is None:
            self.table[hashed_word] = [[word, 1]]
        else:
            for pair in self.table[hashed_word]:
                if pair[0] == word:
                    current_count = pair[1]
                    probability = 1 / (1.1 ** current_count)
                    if random.random() < probability:
                        pair[1] += 1
                    return
            self.table[hashed_word].append([word, 1])

    def get_all_items(self):
        items = []
        for bucket in self.table:
            if bucket is not None:
                items.extend(bucket)
        return items

    def sort(self):
        all_items = self.get_all_items()
        return sorted(all_items, key=lambda x: x[1], reverse=True)


random.seed(0)
NUM_WORDS = 1_000_000

generator = WordStreamGenerator(initial_words=100, max_words=200)
stream = generator.stream_words()

recent_words = deque(maxlen=NUM_WORDS)

normal_hash_table = NormalHashTable(1009)  # Prime size to reduce collisions
log_hash_table = LogHashTable(1009)

start_time = time.perf_counter()
for _ in range(NUM_WORDS):
    word = next(stream)
    normal_hash_table.insert(word)
    log_hash_table.insert(word)

normal_sorted_items = normal_hash_table.sort()
log_sorted_items = log_hash_table.sort()

end_time = time.perf_counter()
print(f"Time to process: {end_time - start_time} seconds")

def log_count_to_real_count(log_count, base=1.1):
    return round(base ** log_count)

values_normal = [count for _, count in normal_sorted_items]
print("\nTop 50 words (Normal Counter):")
for i in range(50):
    word, count = normal_sorted_items[i]
    print(f"{word}: {count}")


values_log = [log_count_to_real_count(log_count) for _, log_count in log_sorted_items]
print("\nTop 50 words (Logarithmic Counter):")
for i in range(50):
    word, log_count = log_sorted_items[i]
    true_count = log_count_to_real_count(log_count)
    print(f"{word}: {true_count}")

import matplotlib.pyplot as plt

ratio = [values_log[i] / values_normal[i] for i in range(50)]

plt.figure(figsize=(12, 6))
plt.plot(values_normal[:50], label="Normal Counter")
plt.plot(values_log[:50], label="Logarithmic Counter")
# plt.plot(ratio, label="Logarithmic/Normal Ratio") uncomment this line to see the ratio
plt.legend()
plt.xlabel("Word Rank")
plt.ylabel("Word Count")
plt.title("Word count comparison")
plt.show()
