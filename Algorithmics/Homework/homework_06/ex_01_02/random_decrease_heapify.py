import random
import time
import matplotlib.pyplot as plt


def heapify_k_ary(arr, n, i, k):
    largest = i
    children = [k * i + j + 1 for j in range(k)]
    for child in children:
        if child < n and arr[child] > arr[largest]:
            largest = child

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify_k_ary(arr, n, largest, k)



def build_k_ary_heap(arr, k):
    n = len(arr)
    for i in range(n // k - 1, -1, -1):
        heapify_k_ary(arr, n, i, k)


def build_k_ary_heap_bubble_up(arr, k):
    n = len(arr)
    for i in range(1, n):
        j = i
        parent = (j - 1) // k
        while j > 0 and arr[j] > arr[parent]:
            arr[j], arr[parent] = arr[parent], arr[j]
            j = parent
            parent = (j - 1) // k

def random_decrease(arr):
    n = len(arr)
    index = random.randint(0, n - 1)
    decrease_value = random.randint(1, 100)
    arr[index] = max(1, arr[index] - decrease_value)


def measure_heapify_time_k_ary(data, k):
    random_decrease(data)
    start = time.time()
    build_k_ary_heap(data, k)
    end = time.time()
    return end - start

def measure_heapify_time_k_ary_bubble_up(data, k):
    random_decrease(data)
    start = time.time()
    build_k_ary_heap_bubble_up(data, k)
    end = time.time()
    return end - start

times_results_heapify = {}
times_results_bubble_up = {}

k_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]

for k in k_values:
    times_results_heapify[k] = []
    times_results_bubble_up[k] = []
    for i in [1000, 10000, 100000, 1000000]:
        data = [random.randint(1, 1000000) for _ in range(i)]

        elapsed_time_heapify = measure_heapify_time_k_ary(data.copy(), k)
        times_results_heapify[k].append(elapsed_time_heapify)

        elapsed_time_bubble_up = measure_heapify_time_k_ary_bubble_up(data.copy(), k)
        times_results_bubble_up[k].append(elapsed_time_bubble_up)

for k in k_values:
    plt.plot([1000, 10000, 100000, 1000000], times_results_heapify[k], label=f'heapify, k={k}')
    plt.plot([1000, 10000, 100000, 1000000], times_results_bubble_up[k], label=f'bubble_up, k={k}')

plt.xlabel('Number of elements')
plt.ylabel('Time (seconds)')
plt.title('Heap Construction Time with Random Decrease (k-ary Heap)')
plt.legend()
plt.grid(True)
plt.show()
