import numpy as np
import matplotlib.pyplot as plt
import time
import math
import random

# Define function choices
f_choices = {
    "n": lambda n: n,
    "n log(n)": lambda n: n * math.log(n),
    "n^2": lambda n: n ** 2,
    "n^2.5": lambda n: n ** 2.5,
    "n^3": lambda n: n ** 3,
    "n^4": lambda n: n ** 4
}


# Define the memoized_T function
def memoized_T(a, b, f, n):
    memo = {}

    def T(n):
        if n in memo:
            return memo[n]
        if n < 10:  # Base case for n < 10
            result = n
        else:
            result = a * T(n // b) + f(n)
        memo[n] = result
        return result

    T(n)  # Run T(n) for the input n
    return memo


# Define the not_memoized_T2 function
def not_memoized_T2(a, b, f, n):
    memo = {}

    def T2(n):
        # if n in memo: return memo[n]           # Not using memoization if commented out
        if n < 10:  # Base case for n < 10
            result = n
        else:
            result = T2(n // b) + T2(n // b) + f(n)
        memo[n] = result
        return result

    T2(n)  # Run T2(n) for the input n
    return memo


# Measure time and collect results for each n value
def measure_time_for_each_n(func, a, b, f, n_values):
    times = []
    for n in n_values:
        start_time = time.time()
        func(a, b, f, n)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
    return times


# Generate a list of random n values between 2^5 and 2^15
random_n_values = [i for i in range(0, 100, 5)]

# Define the parameters for the memoized_T function
a = 2
b = 1 + random.randint(1, 5) / 5

# Measure time for both memoized and non-memoized functions
for function in f_choices:
    name_f, f_func = function, f_choices[function]

    # Measure times for each n value
    memo_times = measure_time_for_each_n(memoized_T, a, b, f_func, random_n_values)
    not_memo_times = measure_time_for_each_n(not_memoized_T2, a, b, f_func, random_n_values)

    # Create a new plot for each function
    plt.figure(figsize=(8, 5))

    # Plot memoized times
    plt.plot(random_n_values, memo_times, label=f"{name_f} (Memoized)")

    # Plot non-memoized times
    plt.plot(random_n_values, not_memo_times, label=f"{name_f} (Non-memoized)")

    # Plot settings
    plt.xlabel("n")
    plt.ylabel("Time (seconds)")
    plt.title(f"Memoized vs Non-Memoized Time for {name_f} (a={a}, b={b:.2f})")
    plt.legend()
    plt.yscale('log')  # Use logarithmic scale for better visualization
    plt.grid(True)

    # Show each plot separately
    plt.show()

    plt.savefig(f"memoized_vs_non_memoized_{name_f}.png")
