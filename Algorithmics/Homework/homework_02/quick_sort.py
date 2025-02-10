import random
import time
import sys

sys.setrecursionlimit(2500)

# List of small precision integers random numbers
small_precision_integers = [random.randint(-10 ** 3, 10 ** 3) for _ in range(10 ** 6)]
s_i = small_precision_integers.copy()
s_i.sort()

# List of large precision integers random numbers
large_precision_integers = [random.randint(-10 ** 6, 10 ** 6) for _ in range(10 ** 6)]
l_i = large_precision_integers.copy()
l_i.sort()

# List of small precision floating point numbers
small_floating_point_numbers = [random.uniform(-10 ** 3, 10 ** 3) for _ in range(10 ** 6)]
s_f = small_floating_point_numbers.copy()
s_f.sort()

# List of large precision floating point numbers
large_precision_floating_point_numbers = [random.uniform(-10 ** 6, 10 ** 6) for _ in range(-10 ** 6, 10 ** 6)]
l_f = large_precision_floating_point_numbers.copy()
l_f.sort()


def dual_pivot_quicksort(arr, low, high):
    if low < high:
        # Choose random pivots
        pivot1_index, pivot2_index = choose_random_pivots(low, high)
        arr[low], arr[pivot1_index] = arr[pivot1_index], arr[low]
        arr[high], arr[pivot2_index] = arr[pivot2_index], arr[high]

        # Ensure pivot1 is less than pivot2
        if arr[low] > arr[high]:
            arr[low], arr[high] = arr[high], arr[low]

        # Partition the array
        piv = partition(arr, low, high)
        # Recursively sort the sub-arrays
        dual_pivot_quicksort(arr, low, piv[0] - 1)
        dual_pivot_quicksort(arr, piv[0] + 1, piv[1] - 1)
        dual_pivot_quicksort(arr, piv[1] + 1, high)

def partition(arr, low, high):
    pivot1 = arr[low]
    pivot2 = arr[high]

    if pivot1 > pivot2:
        pivot1, pivot2 = pivot2, pivot1
        arr[low], arr[high] = arr[high], arr[low]

    lt = low + 1
    gt = high - 1
    i = low + 1

    while i <= gt:
        if arr[i] < pivot1:
            arr[i], arr[lt] = arr[lt], arr[i]
            lt += 1
        elif arr[i] > pivot2:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
            i -= 1
        i += 1

    lt -= 1
    gt += 1

    arr[low], arr[lt] = arr[lt], arr[low]
    arr[high], arr[gt] = arr[gt], arr[high]

    return lt, gt


def choose_random_pivots(low, high):
    pivot1_index = random.randint(low, high)
    pivot2_index = random.randint(low, high)
    while pivot2_index == pivot1_index:
        pivot2_index = random.randint(low, high)
    return pivot1_index, pivot2_index


# Sort the list using the quick sort algorithm
def quickSort(arr, low, high):
    if high <= low:
        return

    pivot_index = random.randint(low, high)  # random pivot selection
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]  # move pivot to end
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    pivot_index = i + 1

    quickSort(arr, low, pivot_index - 1)
    quickSort(arr, pivot_index + 1, high)

def run_simulation(array, sorted_array):
    avg_built_in_1 = 0
    avg_built_in_2 = 0
    avg_quicksort_1 = 0
    avg_quicksort_2 = 0
    avg_quicksort_2_pivots = 0
    # Let's compare the two sorting methods
    print( "# Built-in 1")
    for i in range(3):
      numbers = array.copy()
      start_time = time.time()
      numbers.sort()
      end_time = time.time()
      avg_built_in_1 += end_time - start_time
    avg_built_in_1 /= 3

    print( "# Built-in 2")
    numbers = array.copy()
    for i in range(3):
      start_time = time.time()
      numbers.sort()
      end_time = time.time()
      avg_built_in_2 += end_time - start_time
    avg_built_in_2 /= 3

    print( "# Quicksort 1")
    for i in range(3):
      numbers = array.copy()
      start_time = time.time()
      quickSort( numbers, 0, len(numbers)-1 )
      end_time = time.time()
      avg_quicksort_1 += end_time - start_time
      if numbers == sorted_array:
        pass
        # print("OK - Quicksort was correct")
      else:
        print("Error: Quicksort code was wrong")
    avg_quicksort_1 /= 3

    print( "# Quicksort 2")
    numbers = array.copy()
    for i in range(3):
      start_time = time.time()
      quickSort( numbers, 0, len(numbers)-1 )
      end_time = time.time()
      avg_quicksort_2 += end_time - start_time
    avg_quicksort_2 /= 3

    print( "# Quicksort 2-pivots")
    for i in range(3):
        numbers = array.copy()
        start_time = time.time()
        dual_pivot_quicksort( numbers, 0, len(numbers)-1 )
        end_time = time.time()
        avg_quicksort_2_pivots += end_time - start_time
    avg_quicksort_2_pivots /= 3

    return avg_built_in_1, avg_built_in_2, avg_quicksort_1, avg_quicksort_2, avg_quicksort_2_pivots



# Run the simulation
avg_built_in_1, avg_built_in_2, avg_quicksort_1, avg_quicksort_2, avg_quicksort_2_pivots = run_simulation(small_precision_integers, s_i)
print(f"Small precision integers average time for built-in 1: {avg_built_in_1}")
print(f"Small precision integers average time for built-in 2: {avg_built_in_2}")
print(f"Small precision integers average time for quicksort 1: {avg_quicksort_1}")
print(f"Small precision integers average time for quicksort 2: {avg_quicksort_2}")
print(f"Small precision integers average time for quicksort 2 pivots: {avg_quicksort_2_pivots}")

print()

avg_built_in_1, avg_built_in_2, avg_quicksort_1, avg_quicksort_2, avg_quicksort_2_pivots = run_simulation(large_precision_integers, l_i)
print(f"Large precision integers average time for built-in 1: {avg_built_in_1}")
print(f"Large precision integers average time for built-in 2: {avg_built_in_2}")
print(f"Large precision integers average time for quicksort 1: {avg_quicksort_1}")
print(f"Large precision integers average time for quicksort 2: {avg_quicksort_2}")
print(f"Large precision integers average time for quicksort 2 pivots: {avg_quicksort_2_pivots}")

print()

avg_built_in_1, avg_built_in_2, avg_quicksort_1, avg_quicksort_2, avg_quicksort_2_pivots = run_simulation(small_floating_point_numbers, s_f)
print(f"Small floating point average for built-in 1: {avg_built_in_1}")
print(f"Small floating point average for built-in 2: {avg_built_in_2}")
print(f"Small floating point average for quicksort 1: {avg_quicksort_1}")
print(f"Small floating point average for quicksort 2: {avg_quicksort_2}")
print(f"Small floating point average for quicksort 2 pivots: {avg_quicksort_2_pivots}")

print()

avg_built_in_1, avg_built_in_2, avg_quicksort_1, avg_quicksort_2, avg_quicksort_2_pivots = run_simulation(large_precision_floating_point_numbers, l_f)
print(f"Large floating point average for built-in 1: {avg_built_in_1}")
print(f"Large floating point average for built-in 2: {avg_built_in_2}")
print(f"Large floating point average for quicksort 1: {avg_quicksort_1}")
print(f"Large floating point average for quicksort 2: {avg_quicksort_2}")
print(f"Large floating point average for quicksort 2 pivots: {avg_quicksort_2_pivots}")
