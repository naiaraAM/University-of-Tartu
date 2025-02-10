import random
import time

import numpy as np
from matplotlib import pyplot as plt

NUM_ELEMENTS = 10000000

# Generate ordered and shuffled arrays
ordered_array = [random.randint(0, NUM_ELEMENTS) for _ in range(NUM_ELEMENTS)]
ordered_array.sort()
shuffled_array = ordered_array.copy()
random.shuffle(shuffled_array)

def binary_lookup(ordered_array, value):
    low = 0
    high = len(ordered_array) - 1
    while low <= high:
        mid = (low + high) // 2
        if ordered_array[mid] == value:
            return mid
        elif ordered_array[mid] < value:
            low = mid + 1
        else:
            high = mid - 1
    return -1  # value not found in the array

def linear_search(shuffled_array, value):
    for i in range(len(shuffled_array)):
        if shuffled_array[i] == value:
            return i
    return -1  # value not found in the array

def rank_lookup(ordered_array, value):
    index = binary_lookup(ordered_array, value)
    return index if index != -1 else None

def value_by_rank(ordered_array, rank):
    if 0 <= rank < len(ordered_array):
        return ordered_array[rank]
    return None

# Perform lookups and rank queries within 1 minute
if __name__ == "__main__":
    """
    start_time = time.time()
    end_time = start_time + 60

    # Linear search and rank queries on shuffled array
    num_linear_searches = 0
    num_linear_rank_queries = 0
    while time.time() < end_time:
        value = random.randint(0, NUM_ELEMENTS)
        linear_search(shuffled_array, value)
        num_linear_searches += 1

        rank = random.randint(0, NUM_ELEMENTS - 1)
        value_by_rank(shuffled_array, rank)
        num_linear_rank_queries += 1

    print(f"Number of linear searches: {num_linear_searches}")
    print(f"Number of linear rank queries: {num_linear_rank_queries}")

    # Binary search and rank queries on ordered array
    num_binary_searches = 0
    num_binary_rank_queries = 0
    start_time = time.time()
    end_time = start_time + 60
    while time.time() < end_time:
        value = random.randint(0, NUM_ELEMENTS)
        binary_lookup(ordered_array, value)
        num_binary_searches += 1

        rank = random.randint(0, NUM_ELEMENTS - 1)
        value_by_rank(ordered_array, rank)
        num_binary_rank_queries += 1

    print(f"Number of binary searches: {num_binary_searches}")
    print(f"Number of binary rank queries: {num_binary_rank_queries}")

"""

    # perform given number of lookups and rank queries and measu

    time_ordered = [0] * 20
    time_unordered = [0] * 20
    for i in range(20):
        value = random.randint(0, NUM_ELEMENTS)
        for j in range(10):
            start_time = time.time()
            value_by_rank(ordered_array, value)

            time_ordered[i] += time.time() - start_time
        time_ordered[i] /= 10

        for j in range(10):
            start_time = time.time()
            value_by_rank(shuffled_array, value)
            time_unordered[i] += time.time() - start_time
        time_unordered[i] /= 10


    # time to miliseconds
    time_ordered = [i * 1000 for i in time_ordered]
    time_unordered = [i * 1000 for i in time_unordered]

    # plot the results
    plt.plot(time_ordered, label='Ordered Array')
    plt.plot(time_unordered, label='Shuffled Array')

    # Adding labels and title
    plt.xlabel('Number of Queries')
    plt.ylabel('Time (s)')
    plt.title('Time of Execution by Number of Queries')
    plt.legend()


    # Display the plot
    plt.show()
    plt.close()