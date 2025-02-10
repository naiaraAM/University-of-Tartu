import random

import numpy as np
import matplotlib.pyplot as plt

random.seed(5)

# Generate 20 time series with a random number of cycles between 3 and 7
num_series = 20  # Number of time series to generate
lengths = np.random.randint(20, 50, num_series)  # Varied lengths for each series
cycle_counts = np.random.randint(2, 8, num_series)  # Random cycles between 3 and 7

variable_cycle_time_series = []

for length, cycles in zip(lengths, cycle_counts):
    # Generate random cycle lengths that sum up to the series length
    cycle_lengths = np.random.randint(1, int(length / cycles), cycles)
    cycle_lengths = np.append(cycle_lengths, length - sum(cycle_lengths)).clip(min=1)

    # Generate sinusoidal sections with these random cycle lengths
    series = []
    for cycle_length in cycle_lengths:
        x = np.linspace(0, np.pi, cycle_length)  # Half-cycle (up/down)
        cycle = np.sin(x) + 0.1 * np.random.randn(cycle_length)  # Add some noise
        series.extend(cycle)

    # Ensure the series has the exact target length, starts, and ends at 0
    series = np.array(series[:length])
    series[0] = 0
    series[-1] = 0
    variable_cycle_time_series.append(series)

# Randomly select 3 time series for plotting
sample_indices = np.random.choice(num_series, 3, replace=False)

# Plot the selected subset of time series
plt.figure(figsize=(10, 6))
for i in sample_indices:
    plt.plot(variable_cycle_time_series[i], label=f"Time Series {i+1}")

# Add title, labels, and legend
plt.title("Subset of Time Series with Random Cycle Counts and Lengths")
plt.xlabel("Time Step")
plt.ylabel("Value")
plt.legend()
plt.show()

# Outputting the list of all 20 generated time series
variable_cycle_time_series