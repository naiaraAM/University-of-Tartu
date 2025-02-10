import random
import time
import matplotlib.pyplot as plt

def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def build_heap(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

def build_heap_bubble_up(arr):
    n = len(arr)
    for i in range(1, n):
        j = i
        while j > 0 and arr[j] > arr[(j - 1) // 2]:
            arr[j], arr[(j - 1) // 2] = arr[(j - 1) // 2], arr[j]
            j = (j - 1) // 2

def measure_heapify_time(data):
    start = time.time()
    build_heap(data)
    end = time.time()
    return end - start
def measure_heapify_time_bubble_up(data):
    start = time.time()
    build_heap_bubble_up(data)
    end = time.time()
    return end - start


times_results_heapify = {}
time_results_bubble_up = {}

for i in range(1000, 20000, 50000):
    data = [random.randint(1, 1000000) for _ in range(i)]
    elapsed_time_heapify = measure_heapify_time(data)
    times_results_heapify[i] = elapsed_time_heapify
    elapsed_time_bubble_up = measure_heapify_time_bubble_up(data)
    time_results_bubble_up[i] = elapsed_time_bubble_up



plt.plot(list(times_results_heapify.keys()), list(times_results_heapify.values()), label='heapify')
plt.plot(list(time_results_bubble_up.keys()), list(time_results_bubble_up.values()), label='bubble_up')
plt.xlabel('Number of elements')
plt.ylabel('Time')
plt.legend()
plt.show()