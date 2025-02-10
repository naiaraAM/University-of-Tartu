import random
import matplotlib.pyplot as plt
import time
import math

f_functions = {
    "n": lambda n: n,
    "n log(n)": lambda n: n * math.log(n),
    "n^2": lambda n: n ** 2,
    "n^2.5": lambda n: n ** 2.5,
    "n^3": lambda n: n ** 3,
    "n^4": lambda n: n ** 4
}

a_choices = []
b_choices = []
f_choice_name = []
f_choice_func = []

while len(a_choices) < 3:
    a = random.randint(1, 5)
    if a not in a_choices:
        a_choices.append(a)

while len(b_choices) < 3:
    b = 1 + random.randint(1, 5) / 5
    if b not in b_choices:
        b_choices.append(b)

while len(f_choice_name) < 3:
    f_n, f_f = random.choice(list(f_functions.items()))
    if f_n not in f_choice_name:
        f_choice_name.append(f_n)
        f_choice_func.append(f_f)

n_values = [i for i in range(0, 50)]

memo_T1 = {}
memo_T2 = {}
memo_T3 = {}

def T1(n):
    f = f_choice_func[0]
    if n in memo_T1:
        return memo_T1[n]
    if n < 10:  # Base case for n < 10
        result = n
    else:
        result = a_choices[0] * T2(n // b_choices[0]) + f(n)
    memo_T1[n] = result
    return result

def T2(n):
    f = f_choice_func[1]
    if n in memo_T2:
        return memo_T2[n]
    if n < 10:  # Base case for n < 10
        result = n
    else:
        result = a_choices[1] * T2(n // b_choices[1]) + f(n)
    memo_T2[n] = result
    return result

def T3(n):
    f = f_choice_func[2]
    if n in memo_T3:
        return memo_T3[n]
    if n < 10:  # Base case for n < 10
        result = n
    else:
        result = a_choices[2] * T1(n // b_choices[2]) + f(n)
    memo_T3[n] = result 
    return result

# Measure time and collect results for memoized_T
def measure_time_and_collect_results(func, n_values):
    combined_memo = {}
    start_time = time.time()
    for n in n_values:
        result = func(n)
        combined_memo[n] = result  # Merge new results into the combined memo
    elapsed_time = time.time() - start_time
    return combined_memo, elapsed_time

# Measure time for memoized_T
memo_T, time_T = measure_time_and_collect_results(T1, n_values)
nemo_2_T, time_T2 = measure_time_and_collect_results(T2, n_values)
nemo_3_T, time_T3 = measure_time_and_collect_results(T3, n_values)

# Plotting the results as lines for all functions on the same graph
plt.figure(figsize=(10, 5))

# Using 'plot' to draw lines and marker='o' to show dots at data points
plt.plot(list(memo_T.keys()), list(memo_T.values()), color='blue', label=f"a = {a_choices[0]}, b = {b_choices[0]}, f(n) ={f_choice_name[0]}")
plt.plot(list(nemo_2_T.keys()), list(nemo_2_T.values()), color='red', label=f"a = {a_choices[1]}, b = {b_choices[1]}, f(n) ={f_choice_name[1]}")
plt.plot(list(nemo_3_T.keys()), list(nemo_3_T.values()), color='green', label=f"a = {a_choices[2]}, b = {b_choices[2]}, f(n) ={f_choice_name[2]}")

# Set logarithmic scale on the y-axis to better visualize large differences in growth
plt.yscale('log')

plt.title("n vs T(n) for Different f(n) Functions")
plt.xlabel("n")
plt.ylabel("T(n)")
plt.legend()
plt.grid(True)
plt.show()