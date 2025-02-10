import random
import time
import numpy as np

from matplotlib import pyplot as plt


class KaryHeap:
    def __init__(self, k):
        self.k = k  # number of children for each node
        self.heap = []

    def parent(self, i):
        if i == 0:
            return None  # Root has no parent
        return (i - 1) // self.k

    def children(self, i):
        """Returns the indices of the children of node i."""
        return [self.k * i + j + 1 for j in range(self.k) if self.k * i + j + 1 < len(self.heap)]

    def heapify_down(self, i):
        """Ensures the heap property by moving downwards from node i."""
        smallest = i
        child_indices = self.children(i)

        for child in child_indices:
            if self.heap[child] < self.heap[smallest]:
                smallest = child

        if smallest != i:
            # Swap with the smallest child and heapify down recursively
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.heapify_down(smallest)

    def heapify_up(self, i):
        """Ensures the heap property by moving upwards from node i."""
        parent_idx = self.parent(i)
        if parent_idx is not None and self.heap[i] < self.heap[parent_idx]:
            # Swap the current node with its parent
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            self.heapify_up(parent_idx)

    def insert(self, value):
        """Inserts a value into the heap and ensures the heap property."""
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def extract_min(self):
        """Removes and returns the minimum element from the heap."""
        if len(self.heap) == 0:
            return None  # Heap is empty

        min_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heapify_down(0)
        return min_val
    def sort(self):
        """Sorts the heap in-place."""
        sorted_heap = []
        while self.heap:
            sorted_heap.append(self.extract_min())
        self.heap = sorted_heap


def experiment(k_values, num_elements=10000):
    results = {}
    for k in k_values:
        heap = KaryHeap(k)
        random_integers = random.sample(range(1_000_000_000), num_elements)

        # Insertion phase
        start_time = time.time()
        for value in random_integers:
            heap.insert(value)
        insert_time = time.time() - start_time

        # Sorting phase
        start_time = time.time()
        heap.sort()
        sort_time = time.time() - start_time

        # Extraction phase
        start_time = time.time()
        while heap.heap:
            heap.extract_min()
        extract_time = time.time() - start_time

        results[k] = {"insert_time": insert_time, "sort_time": sort_time, "extract_time": extract_time}

    return results

if __name__ == "__main__":
    k_values = np.arange(2, 20)
    results = experiment(k_values)
    for k, result in results.items():
        print(f"Results for k={k}")
        print(f"Insertion time: {result['insert_time']:.4f} seconds")
        print(f"Sort time: {result['sort_time']:.4f} seconds")
        print(f"Extraction time: {result['extract_time']:.4f} seconds")
        print()
    # plot the results lines
    plt.figure()
    #plt.plot(k_values, [results[k]["insert_time"] for k in k_values], label="Insertion time")
    plt.plot(k_values, [results[k]["sort_time"] for k in k_values], label="Sort time")
    plt.plot(k_values, [results[k]["extract_time"] for k in k_values], label="Extraction time")
    plt.xlabel("k")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.savefig("k-ary_heap_performance_log.png")
    plt.show()
    plt.close()
