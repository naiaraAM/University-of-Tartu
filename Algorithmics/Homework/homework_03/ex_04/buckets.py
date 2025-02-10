import math

import numpy as np
from numpy import ndarray


def generate_points_in_sphere(n_points, radius):
    points = []
    while len(points) < n_points:
        x = np.random.uniform(-radius, radius, n_points)
        y = np.random.uniform(-radius, radius, n_points)
        z = np.random.uniform(-radius, radius, n_points)

        distances = np.sqrt(x**2 + y**2 + z**2)
        inside_sphere = distances <= radius
        valid_points = np.vstack((x[inside_sphere], y[inside_sphere], z[inside_sphere])).T

        points.extend(valid_points)
        # n_points -= len(valid_points)

    return np.array(points)

def calculate_distance_to_center(point: ndarray): # point is in the form [x y z] no comma
    return math.sqrt(sum([coord ** 2 for coord in point]))

def calculate_distances(points):
    return [calculate_distance_to_center(point) for point in points]

def assign_to_buckets(points, distances, boundaries):
    buckets = {}
    for i, point in enumerate(points):
        distance = distances[i]
        for j, (low, high) in enumerate(boundaries):
            if low <= distance < high:
                if j not in buckets:
                    buckets[j] = []
                buckets[j].append(point)
                break
    return buckets

def distribute_in_n_buckets(points, n_buckets, boundaries):
    distances = calculate_distances(points)
    return assign_to_buckets(points, distances, boundaries)

def equi_distant_boundaries(max_distance, n_buckets):
    return [(i * max_distance / n_buckets, (i + 1) * max_distance / n_buckets) for i in range(n_buckets)]

def equi_size_boundaries(distances, n_buckets):
    sorted_distances = sorted(distances)
    bucket_size = len(distances) // n_buckets
    boundaries = [(sorted_distances[i * bucket_size], sorted_distances[(i + 1) * bucket_size - 1]) for i in range(n_buckets)]
    boundaries[-1] = (boundaries[-1][0], max(distances))
    return boundaries

def further_split_buckets(buckets, n_sub_buckets):
    sub_buckets = {}
    for i, bucket_points in buckets.items():
        bucket_distances = calculate_distances(bucket_points)
        max_bucket_distance = max(bucket_distances)
        min_bucket_distance = min(bucket_distances)
        sub_boundaries = [(min_bucket_distance + j * (max_bucket_distance - min_bucket_distance) / n_sub_buckets,
                           min_bucket_distance + (j + 1) * (max_bucket_distance - min_bucket_distance) / n_sub_buckets)
                          for j in range(n_sub_buckets)]

        sub_buckets[i] = assign_to_buckets(bucket_points, bucket_distances, sub_boundaries)
    return sub_buckets

# Generate points
n_points = 10000
radius = 1000
points = generate_points_in_sphere(n_points, radius)

# Calculate distances
distances = calculate_distances(points)
max_distance = max(distances)

# Equi-distant boundaries
equi_distant_boundaries_10 = equi_distant_boundaries(max_distance, 10)
buckets_equi_distant = distribute_in_n_buckets(points, 10, equi_distant_boundaries_10)

# Equi-size boundaries
equi_size_boundaries_10 = equi_size_boundaries(distances, 10)
buckets_equi_size = distribute_in_n_buckets(points, 10, equi_size_boundaries_10)

# Further split each bucket into 5 sub-buckets
sub_buckets_equi_distant = further_split_buckets(buckets_equi_distant, 5)
sub_buckets_equi_size = further_split_buckets(buckets_equi_size, 5)

# Count points in each bucket and sub-bucket
def count_points_in_buckets(buckets):
    counts = {}
    for i, sub_buckets in buckets.items():
        counts[i] = {j: len(sub_buckets[j]) for j in sub_buckets}
    return counts

counts_equi_distant = count_points_in_buckets(sub_buckets_equi_distant)
counts_equi_size = count_points_in_buckets(sub_buckets_equi_size)

# Print results with ranges
print("Equi-distant bucket counts and ranges:")
for i, boundary in enumerate(equi_distant_boundaries_10):
    print(f"Bucket {i} ({boundary[0]:.2f} - {boundary[1]:.2f}): {sum(counts_equi_distant.get(i, {}).values())} points")
    for j in range(5):
        sub_boundary = (boundary[0] + j * (boundary[1] - boundary[0]) / 5,
                        boundary[0] + (j + 1) * (boundary[1] - boundary[0]) / 5)
        print(f"  Sub-bucket {j} ({sub_boundary[0]:.2f} - {sub_boundary[1]:.2f}): {counts_equi_distant.get(i, {}).get(j, 0)} points")

print("\nEqui-size bucket counts and ranges:")
for i, boundary in enumerate(equi_size_boundaries_10):
    print(f"Bucket {i} ({boundary[0]:.2f} - {boundary[1]:.2f}): {sum(counts_equi_size.get(i, {}).values())} points")
    for j in range(5):
        sub_boundary = (boundary[0] + j * (boundary[1] - boundary[0]) / 5,
                        boundary[0] + (j + 1) * (boundary[1] - boundary[0]) / 5)
        print(f"  Sub-bucket {j} ({sub_boundary[0]:.2f} - {sub_boundary[1]:.2f}): {counts_equi_size.get(i, {}).get(j, 0)} points")