import random

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

def random_decrease(arr):
    index = random.randint(1, len(arr) - 1)
    arr[index] = random.randint(1, arr[index])
    heapify(arr, len(arr), index)

def report_heap_top_two_layers(arr):
    if len(arr) == 0:
        return "Heap is empty"
    root = arr[0]
    left_child = arr[1] if len(arr) > 1 else None
    right_child = arr[2] if len(arr) > 2 else None
    return f"Root: {root}, Left Child: {left_child}, Right Child: {right_child}"

# Main
k = 10
data = [random.randint(1, 1000000) for _ in range(k)]

build_heap(data)
heapify_report = report_heap_top_two_layers(data)
print(f"After heapify: {heapify_report}")

data = [random.randint(1, 1000000) for _ in range(k)]  # Re-generate data
build_heap_bubble_up(data)
bubble_up_report = report_heap_top_two_layers(data)
print(f"After one-by-one insertions (bubble-up): {bubble_up_report}")

random_decrease(data)
random_decrease_report = report_heap_top_two_layers(data)
print(f"After random decrease: {random_decrease_report}")
