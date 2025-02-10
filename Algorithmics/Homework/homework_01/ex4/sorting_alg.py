from typing import List

from homework_01.ex2_3.random_gen import random_generator_array
from sorting_techniques import pysort
from matplotlib import pyplot as plt


import time

NUM_ELEMENTS_MINUTE = 10000000

def measure_minute_sorting() -> None:
    """
    Measure the time for 25 million elements, aprox one minute.
    """
    sort_obj = pysort.Sorting()
    results = []
    aux_array = random_generator_array(NUM_ELEMENTS_MINUTE)
    total_time = 0

    for j in range(5):
        start_time = time.perf_counter()
        sort_obj.mergeSort(aux_array)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    mean = float(total_time) / 5.0
    print (f"Mean time for sorting {NUM_ELEMENTS_MINUTE} elements: {mean} seconds")


def measure_times_merge_sort() -> List[float]:
    sort_obj = pysort.Sorting()
    results = []
    for i in range(0, 20000000, 500000):
        print(f"{i}")
        aux_array = random_generator_array(i)  # 2 to the power of i
        start_time = time.perf_counter()
        sort_obj.mergeSort(aux_array)
        end_time = time.perf_counter()
        results.append(float(end_time - start_time))
    return results

if __name__ == "__main__":
    # plot for merge sort
    measure_minute_sorting()
    """
    plt.plot(range(2, 26), merge_sort_times)
    plt.xlabel("Power of 2")
    plt.ylabel("Time (s)")
    plt.savefig("merge_sort.png")
    """
# measure_minute_sorting()