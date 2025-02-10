import random
import time
from collections import deque
from Homework.homework_07.ex_03.word_gen import WordStreamGenerator
NUM_WORDS = 1_000_000

generator = WordStreamGenerator(initial_words=100, max_words=200)
stream = generator.stream_words()

recent_words = deque(maxlen=NUM_WORDS)
dict_words = {}

start_time = time.perf_counter()
for _ in range(NUM_WORDS):
    word = next(stream)
    if word in dict_words:
        dict_words[word] += 1
    else:
        dict_words[word] = 1

sorted_dict = sorted(dict_words.items(), key=lambda x: x[1], reverse=True)
end_time = time.perf_counter()
print(f"Time to process: {end_time - start_time} seconds")
for i in range(50):
    print(f"{sorted_dict[i][0]}: {sorted_dict[i][1]}")