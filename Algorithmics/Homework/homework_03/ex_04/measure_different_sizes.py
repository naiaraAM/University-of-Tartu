import math
import time

import matplotlib.pyplot as plt
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

    return np.array(points)

def calculate_distance_to_center(point: ndarray):
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

def count_points_in_buckets(buckets):
    counts = {}
    for i, sub_buckets in buckets.items():
        counts[i] = {j: len(sub_buckets[j]) for j in sub_buckets}
    return counts

def process_points(n_points, radius, n_buckets, n_sub_buckets):
    points = generate_points_in_sphere(n_points, radius)
    distances = calculate_distances(points)
    max_distance = max(distances)

    equi_distant_boundaries_list = equi_distant_boundaries(max_distance, n_buckets)
    buckets_equi_distant = distribute_in_n_buckets(points, n_buckets, equi_distant_boundaries_list)

    equi_size_boundaries_list = equi_size_boundaries(distances, n_buckets)
    buckets_equi_size = distribute_in_n_buckets(points, n_buckets, equi_size_boundaries_list)

    sub_buckets_equi_distant = further_split_buckets(buckets_equi_distant, n_sub_buckets)
    sub_buckets_equi_size = further_split_buckets(buckets_equi_size, n_sub_buckets)

    counts_equi_distant = count_points_in_buckets(sub_buckets_equi_distant)
    counts_equi_size = count_points_in_buckets(sub_buckets_equi_size)

    return counts_equi_distant, counts_equi_size, sub_buckets_equi_distant, sub_buckets_equi_size

def sort_buckets(bucket):
    if len(bucket) <= 10:
        sorted_points = [] * len(bucket)
        for point in bucket:
            distance = calculate_distance_to_center(point)
            sorted_points.append((point, distance))

        sorted_points.sort(key=lambda x: x[1])
        sorted = [point for point, distance in sorted_points]
        return sorted
    else:
        # divide in half and sort each half
        half = len(bucket) // 2
        left = sort_buckets(bucket[:half])
        right = sort_buckets(bucket[half:])

        sorted_points = []
        for i in range(len(left)):
            sorted_points.append(left[i])
        for i in range(len(right)):
            sorted_points.append(right[i])
        return sorted_points

def sort(buckets):
    sorted_points = []
    for keys, bucket in buckets.items():
        for sub_bucket in bucket.values():
            sorted_points.append(sort_buckets(sub_bucket))
    return sorted_points


def sort_quick(buckets):
    sorted_points = []
    for keys, bucket in buckets.items():
        for sub_bucket in bucket.values():
            sorted_points.append(quick_sort(sub_bucket))
    return sorted_points

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        pivot_distance = calculate_distance_to_center(pivot)
        less = [x for x in arr[1:] if calculate_distance_to_center(x) < pivot_distance]
        greater = [x for x in arr[1:] if calculate_distance_to_center(x) >= pivot_distance]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# Example usage:
n_points = 10000
radius = 1000
n_buckets = 10
n_sub_buckets = 5

counts_equi_distant, counts_equi_size, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, n_buckets, n_sub_buckets)

time_equi_distant = []
time_equi_size = []
time_equi_distant_quick = []
time_equi_size_quick = []

_, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, 12, 1)
start = time.time()
sort(sub_buckets_equi_distant)
end = time.time()
time_equi_distant.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_distant)
end = time.time()
time_equi_distant_quick.append(end - start)

start = time.time()
sort(sub_buckets_equi_size)
end = time.time()
time_equi_size.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_size)
end = time.time()
time_equi_size_quick.append(end - start)

_, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, 6, 2)
start = time.time()
sort(sub_buckets_equi_distant)
end = time.time()
time_equi_distant.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_distant)
end = time.time()
time_equi_distant_quick.append(end - start)

start = time.time()
sort(sub_buckets_equi_size)
end = time.time()
time_equi_size.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_size)
end = time.time()
time_equi_size_quick.append(end - start)

_, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, 4, 3)
start = time.time()
sort(sub_buckets_equi_distant)
end = time.time()
time_equi_distant.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_distant)
end = time.time()
time_equi_distant_quick.append(end - start)

start = time.time()
sort(sub_buckets_equi_size)
end = time.time()
time_equi_size.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_size)
end = time.time()
time_equi_size_quick.append(end - start)

_, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, 3, 4)
start = time.time()
sort(sub_buckets_equi_distant)
end = time.time()
time_equi_distant.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_distant)
end = time.time()
time_equi_distant_quick.append(end - start)

start = time.time()
sort(sub_buckets_equi_size)
end = time.time()
time_equi_size.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_size)
end = time.time()
time_equi_size_quick.append(end - start)

_, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, 1, 12)
start = time.time()
sort(sub_buckets_equi_distant)
end = time.time()
time_equi_distant.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_distant)
end = time.time()
time_equi_distant_quick.append(end - start)

start = time.time()
sort(sub_buckets_equi_size)
end = time.time()
time_equi_size.append(end - start)

start = time.time()
sort_quick(sub_buckets_equi_size)
end = time.time()
time_equi_size_quick.append(end - start)

plt.plot(time_equi_distant, label='equi_distant')
plt.plot(time_equi_distant_quick, label='equi_distant_quick')
plt.plot(time_equi_size, label='equi_size')
plt.plot(time_equi_size_quick, label='equi_size_quick')
plt.legend()

plt.xticks(range(5), ['(12, 1)', '(6, 2)', '(4, 3)', '(3, 4)', '(1, 12)'])
plt.savefig('sub_bucket_counts.png')
plt.show()


for i in range (1, 51):
    for j in range(1, 11):
        _, _, sub_buckets_equi_distant, sub_buckets_equi_size = process_points(n_points, radius, i, j)
        start = time.time()
        sort(sub_buckets_equi_distant)
        end = time.time()
        time_equi_distant.append(end - start)

        start = time.time()
        sort_quick(sub_buckets_equi_distant)
        end = time.time()
        time_equi_distant_quick.append(end - start)

        start = time.time()
        sort(sub_buckets_equi_size)
        end = time.time()
        time_equi_size.append(end - start)

        start = time.time()
        sort_quick(sub_buckets_equi_size)
        end = time.time()
        time_equi_size_quick.append(end - start)


plt.plot(time_equi_distant, label='equi_distant')
plt.plot(time_equi_distant_quick, label='equi_distant_quick')
plt.plot(time_equi_size, label='equi_size')
plt.plot(time_equi_size_quick, label='equi_size_quick')
plt.legend()
plt.show()

plt.savefig('sub_bucket_counts.png')





