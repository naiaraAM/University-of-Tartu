import math
import mmh3
import random

from Homework.homework_07.ex_03.word_gen import WordStreamGenerator

class LogCounter:
    def __init__(self):
        self.counter = 0

    def increment(self):
        base = 1.1
        increment_prob = 1 / (base ** self.counter)
        if random.random() < increment_prob and self.counter < 255:
            self.counter += 1

    def decrement(self):
        if self.counter > 0:
            self.counter -= 1

    def is_set(self):
        return self.counter > 0

    def get_value(self):
        base = 1.1
        return base ** self.counter


class CountingBloomFilter:
    def __init__(self, n, p):
        self.n = n  # expec num elements
        self.p = p  # false positive rate
        self.m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2)) # size of the bit array
        self.k = math.ceil((self.m / n) * math.log(2)) # num of hash functions
        self.counters = [LogCounter() for _ in range(self.m)] # log counters

    def add(self, item):
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.m
            self.counters[digest].increment()

    def remove(self, item):
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.m
            self.counters[digest].decrement()

    def check(self, item):
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.m
            if not self.counters[digest].is_set():
                return False
        return True


counting_bloom_filter = CountingBloomFilter(n=1_000_000, p=0.01)

generator = WordStreamGenerator(initial_words=100, max_words=200)
stream = generator.stream_words()

for _ in range(1_000_000):
    word = next(stream)
    counting_bloom_filter.add(word)

false_positives = 0
total_tests = 1_000_000
tested_words = set()

for _ in range(total_tests):
    word = next(stream)
    if word not in tested_words and counting_bloom_filter.check(word):
        # False positive: bloom_filter says "yes", but we've not seen it before
        false_positives += 1
    tested_words.add(word)

false_positive_rate = (false_positives / total_tests) * 100
print(f"False positive rate: {false_positive_rate:.2f}%")
