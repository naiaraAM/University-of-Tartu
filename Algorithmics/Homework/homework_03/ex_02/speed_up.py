import numpy as np
import matplotlib.pyplot as plt
import time
import math
import random

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

# Define the memoized_T2 function
def not_memoized_T2(a, b, f, n):
    memo = {}
    # here a is always 2, since we use T2() + T2()
    def T2(n):
        # if n in memo: return memo[n]           # Let's not use memoization if commented out
        if n < 10:  # Base case for n < 10
            result = n
        else:
            result = T2(n // b) + T2(n // b) + f(n)
        memo[n] = result
        return result

    T2(n)  # Run T2(n) for the input n
    return memo


# Measure time and collect results for both memoized_T and memoized_T2
def measure_time_and_collect_results(func, a, b, f, n_values):
    combined_memo = {}
    start_time = time.time()
    for n in n_values:
        result = func(a, b, f, n)
        combined_memo.update(result)  # Merge new results into the combined memo
    elapsed_time = time.time() - start_time
    return combined_memo, elapsed_time

# Generate a list of random n values between 1000 and 10,000
random_n_values = [2**i for i in range(5, 16)]


# Define the parameters for the memoized_T function
a = 2
b = 1 + random.randint(1, 5) / 5

results = []
# Measure time for memoized_T and memoized_T2
for function in f_choices:

    name_f, name_funct = function, f_choices[function]
    time_T_aux = 0
    time_T2_aux = 0
    for _ in range(5):
        memo_T, time_T = measure_time_and_collect_results(memoized_T, a, b, name_funct, random_n_values)
        memo_T2, time_T2 = measure_time_and_collect_results(not_memoized_T2, a, b, name_funct, random_n_values)
        time_T_aux += time_T
        time_T2_aux += time_T2
    time_T_aux /= 5
    time_T2_aux /= 5

    # Report the measured times
    print(f"Function: T(n) = {a} * T(n / {b}) + {name_f}")
    print(f"Time taken for memoized_T: {time_T_aux:.6f} seconds")
    print(f"Time taken for memoized_T2: {time_T2_aux:.6f} seconds")
    speed_up = time_T_aux / time_T2_aux
    print(f"Speed up: {speed_up:.2f} times")

    results.append((name_f, speed_up))

# Plot the results in a bar chart
plt.figure(figsize=(10, 5))
plt.bar([name_f for name_f, _ in results], [speed_up for _, speed_up in results])
plt.xlabel("Function")
plt.ylabel("Speed up")

plt.savefig("speed_up.png")

plt.show()
plt.close()
