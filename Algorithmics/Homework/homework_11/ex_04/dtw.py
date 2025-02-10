import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import random

random.seed(5)

from Homework.homework_11.ex_04.sample_code import variable_cycle_time_series

def dwt(series1, series2):
    # Calculate the difference between the two series
    difference = series1 - series2

    # Calculate the cumulative sum of the absolute difference
    cumulative_sum = np.cumsum(np.abs(difference))

    # Return the last element of the cumulative sum
    return cumulative_sum[-1]


# Function to count the number of bumps in a time series
def count_bumps(series):
    peaks, _ = find_peaks(series, height=0)  # Find positive peaks
    return len(peaks)

# Group time series by number of bumps
bump_counts = [count_bumps(series) for series in variable_cycle_time_series]
unique_bumps = sorted(set(bump_counts))  # Unique bump counts

# Create a dictionary grouping time series by bump count
grouped_series = {b: [] for b in unique_bumps}
for i, bumps in enumerate(bump_counts):
    grouped_series[bumps].append(variable_cycle_time_series[i])

# Select a group to plot (e.g., series with 4 bumps)
possible_bump_counts = sorted(grouped_series.keys())
for i, bumps in enumerate(possible_bump_counts):

    selected_series = grouped_series[bumps][:4]  # Select up to 4 examples

    # Plot the selected time series
    plt.figure(figsize=(10, 6))
    for i, series in enumerate(selected_series):
        plt.plot(series, label=f"Series {i + 1}")

    plt.title(f"Time Series with {bumps} Bumps")
    plt.xlabel("Time Step")
    plt.ylabel("Value")
    plt.legend()
    plt.show()

    # for each pair of time series in the group, if the series do not have the same number of bumps, calculate the DTW distance between the two series
    for i in range(len(selected_series)):
        for j in range(i + 1, len(selected_series)):
            if count_bumps(selected_series[i]) != count_bumps(selected_series[j]):
                print(f"DTW distance between series {i + 1} and {j + 1}: {dwt(selected_series[i], selected_series[j])}")
# Output the number of bumps in each group
print(f"Bump counts: {bump_counts}")

import numpy as np


def dtw(series1, series2):
    n, m = len(series1), len(series2)
    dtw_matrix = np.full((n + 1, m + 1), float('inf'))
    dtw_matrix[0, 0] = 0

    # Fill the DTW matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(series1[i - 1] - series2[j - 1])
            dtw_matrix[i, j] = cost + min(
                dtw_matrix[i - 1, j],  # Insertion
                dtw_matrix[i, j - 1],  # Deletion
                dtw_matrix[i - 1, j - 1]  # Match
            )

    # Backtrack to find the optimal path
    i, j = n, m
    path = []
    while i > 0 or j > 0:
        path.append((i - 1, j - 1))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            choices = [dtw_matrix[i - 1, j], dtw_matrix[i, j - 1], dtw_matrix[i - 1, j - 1]]
            step = np.argmin(choices)
            if step == 0:
                i -= 1
            elif step == 1:
                j -= 1
            else:
                i -= 1
                j -= 1
    path.reverse()

    return dtw_matrix[n, m], dtw_matrix, path

# calculate distances all to all and save it to a csv with just two decimals, the first row must be the number of bumps
bump_counts = [count_bumps(series) for series in variable_cycle_time_series]
unique_bumps = sorted(set(bump_counts))  # Unique bump counts

# Sort the time series by the number of bumps
sorted_indices = np.argsort(bump_counts)
sorted_series = [variable_cycle_time_series[i] for i in sorted_indices]
sorted_bump_counts = [bump_counts[i] for i in sorted_indices]

# Output the number of bumps in each group
print(f"Sorted bump counts: {sorted_bump_counts}")

# Calculate the DTW distances between all pairs of sorted time series
dtw_distances = np.full((len(sorted_series), len(sorted_series)), np.nan)
for i, series1 in enumerate(sorted_series):
    for j, series2 in enumerate(sorted_series):
        if i < j:
            distance, _, _ = dtw(series1, series2)
            dtw_distances[i, j] = round(distance, 2)
            dtw_distances[j, i] = round(distance, 2)

# Save the DTW distances to a CSV file with the first row as the number of bumps
header = ','.join(map(str, sorted_bump_counts))
np.savetxt("dtw_distances.csv", dtw_distances, fmt="%.2f", delimiter=",", header=header, comments='')
print("DTW distances saved to 'dtw_distances.csv'")
