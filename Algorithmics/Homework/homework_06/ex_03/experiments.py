import heapq
import time
from random import random


def find_kth_smallest_in_stream(stream, k):
    # Using a max-heap of size k
    max_heap = []

    start_time = time.time()  # To measure processing time

    for value in stream:
        if len(max_heap) < k:
            # If heap has less than k elements, push the negative value (to simulate max-heap)
            heapq.heappush(max_heap, -value)
        elif value < -max_heap[0]:
            # If new value is smaller than the current k-th smallest (max of heap)
            heapq.heappushpop(max_heap, -value)

    end_time = time.time()  # End time after processing the stream

    # The k-th smallest element will be the root of the heap (negative sign to restore original value)
    kth_smallest = -max_heap[0] if max_heap else None

    processing_time = end_time - start_time
    return kth_smallest, processing_time


# Example of using the function with Fibonacci data
def fib(data_size, module):
    if data_size == 0:
        return []
    if data_size == 1:
        return [0]

    fib_sequence = [0, 1]
    while len(fib_sequence) < data_size:
        fib_val = (fib_sequence[-1] + fib_sequence[-2]) % module
        fib_sequence.append(fib_val)

    return fib_sequence


# Simulate a stream of 1 million Fibonacci numbers mod 1000
#fib_stream = fib(1000000, 1000000000)
# 1 million random integers between 0 and 1000
random_stream = [int(random() * 1000000000) for _ in range(100000000)]

# Find the kth smallest element
k = 1000000
#kth_smallest_value, time_taken = find_kth_smallest_in_stream(fib_stream, k)
kth_smallest_value, time_taken = find_kth_smallest_in_stream(random_stream, k)
print(f"The {k}-th smallest value is: {kth_smallest_value}")
print(f"Time taken: {time_taken:.6f} seconds")
