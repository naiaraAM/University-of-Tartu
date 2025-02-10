import random
import time
from collections import deque
from Homework.homework_07.ex_03.word_gen import WordStreamGenerator

class HashTable:
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

random.seed(0)  # Set seed for reproducibility
NUM_WORDS = 1_000_000

generator = WordStreamGenerator(initial_words=100, max_words=200)
stream = generator.stream_words()

recent_words = deque(maxlen=NUM_WORDS)
hash_table = HashTable(1009)

start_time = time.perf_counter()
for _ in range(NUM_WORDS):
    word = next(stream)
    hash_table.insert(word)

sorted_items = hash_table.sort()

end_time = time.perf_counter()
print(f"Time to process: {end_time - start_time} seconds")

for i in range(50):
    print(f"{sorted_items[i][0]}: {sorted_items[i][1]}")
