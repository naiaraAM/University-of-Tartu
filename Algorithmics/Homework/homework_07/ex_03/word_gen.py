import random
import string
from collections import defaultdict, deque, Counter

# Global debug level
debug_level = 0  # Set from 0 (no output) to 5+ (detailed output)

# Function to generate a random word
def random_word(length=5):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

# Function to simulate a geometric distribution
def geometric(p):
    """
    Returns a random number based on the geometric distribution with success probability p.
    This returns the number of trials until the first success.
    """
    count = 1
    while random.random() >= p:
        count += count
    return count

# Function to get a skewed frequency using a geometric distribution
def skewed_frequency(p=0.5):
    """
    Returns a skewed frequency based on a geometric distribution.
    Higher probabilities are given to lower values.
    """
    freq = geometric(p)
    return min(freq, 1000)  # Limit the frequency to 100

# Class to generate the word stream
class WordStreamGenerator:
    def __init__(self, initial_words=100, max_words=1000):
        # Dictionary to store words and their frequencies
        self.word_pool = defaultdict(int)
        self.total_words = initial_words
        self.max_words = max_words
        self.baseline_frequency = 1

        # Initialize with a skewed baseline pool of words
        for _ in range(self.total_words):
            word = random_word(random.randint(3, 8))
            self.word_pool[word] = skewed_frequency(0.5)  # Use the skewed frequency

        if debug_level >= 1:
          print(f"Initialized with {len(generator.word_pool)} words.")

    # Method to dynamically add or remove words from the pool
    def adjust_pool(self):
        # Randomly add new words to the pool
        if len(self.word_pool) < self.max_words:
            new_word = random_word(random.randint(3, 8))
            new_freq = skewed_frequency(0.5)
            self.word_pool[new_word] = new_freq
            if new_freq >= 50 and debug_level >= 1:  # Print only for high-frequency new words
                print(f"Added new word with high frequency: {new_word} (freq {new_freq})")

        # Randomly remove some words
        if len(self.word_pool) > self.total_words:
            remove_word = random.choice(list(self.word_pool.keys()))
            del self.word_pool[remove_word]
            if debug_level >= 4:
                print(f"Removed word: {remove_word}")  # Print only at higher debug levels

        # Randomly adjust word frequencies
        for word in list(self.word_pool.keys()):
            # Increase frequencies rapidly for some words
            if random.random() < 0.001:
                change = skewed_frequency(0.8)  # increase
                self.word_pool[word] += change
                if self.word_pool[word] >= 50 and debug_level >= 1:  # Print for high-frequency words
                    print(f"Word '{word}' gained high frequency: {self.word_pool[word]}")

            # Gradually decrease frequencies towards baseline for other words
            if random.random() < 0.01:
                self.word_pool[word] = max(self.baseline_frequency, self.word_pool[word] - random.randint(1, 20))  # Slow decrease

            # With some probability, remove a word
            if random.random() < 0.001:
                if debug_level >= 4:
                    print(f"Removing '{word}' from the pool.")  # Print only at higher debug levels
                del self.word_pool[word]

    # Method to generate a word based on current frequencies
    def generate_word(self):
        words, frequencies = zip(*self.word_pool.items())
        total_frequency = sum(frequencies)
        probabilities = [freq / total_frequency for freq in frequencies]

        # Choose a word based on the probabilities
        chosen_word = random.choices(words, probabilities, k=1)[0]
        return chosen_word

    # Infinite stream generator
    def stream_words(self):
        while True:
            # Emit a word
            word = self.generate_word()
            yield word

            # Occasionally adjust the pool of words and their frequencies
            if random.random() < 0.05:
                self.adjust_pool()