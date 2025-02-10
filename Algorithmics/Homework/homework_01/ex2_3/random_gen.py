from random import randint
import time
from typing import List, Tuple
from matplotlib import pyplot as plt

N_MIN = -100
N_MAX = 100


def random_generator_array(num_elements: int) -> List[int]:
    """
    Generate list of size num_elements in between a range
    """
    output = []

    for i in range(num_elements):
        output.append(randint(N_MIN, N_MAX))
    return output

def calculate_odd_sum(series: list) -> int:
    """
    Calculate sum of odd integers within the list
    """
    total_sum = 0

    for val in series:
        if val % 2 != 0:
            total_sum += val

    return total_sum


def measure_times_power_of_two() -> List[float]:
    """
    Returns an array of obtained values after time measure.
    """
    results = []

    for i in range (2, 26):
        print(f"Calculating for 2^{i}")
        aux_array = random_generator_array(2 ** i)  # 2 to the power of i
        total_time = 0
        for j in range(5):
            start_time = time.perf_counter()
            calculate_odd_sum(aux_array)
            end_time = time.perf_counter()
            total_time += end_time - start_time
        mean = float(total_time) / 5.0
        results.append(mean)
    return results


def measure_times_fixed_size(array_size: int) -> Tuple[List[float], List[float]]:
    """
    Returns a tuple of arraya of obtained values after time measure.
    """
    results_fixed = []
    results_variable = []
    print(f"Calculating for {array_size}")
    fixed_aux_array = random_generator_array(array_size)

    for i in range(50):
        aux_array_variable = random_generator_array(array_size)  # given size
        start_time_variable = time.perf_counter()
        calculate_odd_sum(aux_array_variable)
        end_time_variable = time.perf_counter() - start_time_variable
        results_variable.append(end_time_variable)

    for i in range(50):
        sum_times_fixed = 0
        for j in range(5):
            start_time_fixed = time.perf_counter()
            calculate_odd_sum(fixed_aux_array)
            end_time_fixed = time.perf_counter() - start_time_fixed
            sum_times_fixed += end_time_fixed
        results_fixed.append(float(sum_times_fixed) / 5.0)
    return results_fixed, results_variable


if __name__ == "__main__":
    """
    power_of_two_times = measure_times_power_of_two()
    plt.plot(range(2, 26), power_of_two_times)
    plt.xlabel("Power of 2")
    plt.ylabel("Time (s)")
    plt.title("Time vs Power of 2")
    plt.savefig("power_of_two.png")
    plt.close()
"""
    fixed_size_times = measure_times_fixed_size(500000)
    plt.plot(range(0, 50), fixed_size_times[0])
    plt.plot(range(0, 50), fixed_size_times[1])
    plt.xlabel("Num iterations")
    plt.ylabel("Time (s)")
    plt.title("Time vs Size")
    plt.legend(["Fixed array", "Variable array"])
    plt.savefig("fixed_size.png")
    plt.close()