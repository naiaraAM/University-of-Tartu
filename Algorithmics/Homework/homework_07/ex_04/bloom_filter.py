import math
import mmh3
from bitarray import bitarray

from Homework.homework_07.ex_03.word_gen import WordStreamGenerator


class BloomFilter:
    def __init__(self, n, p):
        self.n = n # expec num elements
        self.p = p # false positive rate
        self.m = math.ceil(-(n * math.log(p)) / (math.log(2) ** 2)) # size of the bit array
        self.k = math.ceil((self.m / n) * math.log(2)) # num hash functions
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

    def add(self, item):
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.m
            self.bit_array[digest] = 1

    def check(self, item):
        for i in range(self.k):
            digest = mmh3.hash(item, i) % self.m
            if not self.bit_array[digest]:
                return False
        return True


bloom_filter = BloomFilter(n=1_000_000, p=0.01)
generator = WordStreamGenerator(initial_words=100, max_words=200)
stream = generator.stream_words()

for _ in range(1_000_000):
    word = next(stream)
    bloom_filter.add(word)

false_positives = 0
total_tests = 1_000_000
tested_words = set()

for _ in range(total_tests):
    word = next(stream)
    if word not in tested_words and bloom_filter.check(word):
        false_positives += 1
    tested_words.add(word)

false_positive_rate = (false_positives / total_tests) * 100
print(f"False positive rate: {false_positive_rate:.2f}%")
