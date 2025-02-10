import os
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import multiprocessing

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def total_distance(tour, points):
    dist = 0
    for i in range(len(tour) - 1):
        dist += euclidean_distance(points[tour[i]], points[tour[i + 1]])
    dist += euclidean_distance(points[tour[-1]], points[tour[0]])  # Return to start
    return dist

def nearest_neighbor_tsp(points):
    n = len(points)
    visited = [False] * n
    tour = [0]  # Start from the first point
    visited[0] = True
    current_city = 0

    for _ in range(n - 1):
        nearest_city = None
        nearest_distance = float('inf')
        for city in range(n):
            if not visited[city]:
                distance = euclidean_distance(points[current_city], points[city])
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_city = city
        tour.append(nearest_city)
        visited[nearest_city] = True
        current_city = nearest_city

    return tour

def two_opt(tour, points):
    n = len(tour)
    best_tour = tour[:]
    best_distance = total_distance(best_tour, points)

    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if j - i == 1: continue  # Skip adjacent edges
            new_tour = best_tour[:]
            new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
            new_distance = total_distance(new_tour, points)

            if new_distance < best_distance:
                best_tour = new_tour
                best_distance = new_distance

    return best_tour

def simulated_annealing(points, initial_tour, initial_temperature=1000, cooling_rate=0.995, max_iter=1000):
    current_tour = initial_tour
    current_distance = total_distance(current_tour, points)
    temperature = initial_temperature

    best_tour = current_tour
    best_distance = current_distance

    for _ in range(max_iter):
        new_tour = two_opt(current_tour, points)
        new_distance = total_distance(new_tour, points)

        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_tour = new_tour
            current_distance = new_distance

            if current_distance < best_distance:
                best_tour = current_tour
                best_distance = current_distance

        temperature *= cooling_rate

    return best_tour, best_distance

def read_file(file_path):
    points = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            point_id, x, y = line.strip().split()
            points.append((point_id, float(x), float(y)))
    return points

def parse_points(point_data):
    points = []
    labels = []
    for label, x, y in point_data:
        labels.append(label)
        points.append((float(x), float(y)))
    return labels, points

def plot_tsp(points, tour):
    x, y = zip(*points)
    plt.scatter(x, y, color='red', s=10)

    for i in range(len(tour) - 1):
        p1 = points[tour[i]]
        p2 = points[tour[i + 1]]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', lw=2)

    p1 = points[tour[-1]]
    p2 = points[tour[0]]
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', lw=2)

    plt.title("TSP Tour with Simulated Annealing and 4-opt Optimization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def parallel_simulated_annealing(points, initial_tour, n_processes=12):
    with multiprocessing.Pool(processes=n_processes) as pool:
        results = pool.starmap(simulated_annealing, [(points, initial_tour) for _ in range(n_processes)])

    best_tour, best_distance = min(results, key=lambda x: x[1])
    return best_tour, best_distance

def main():
    current_dir = os.path.dirname(__file__)
    filenames = ['../hw10_tsp_points_data_0030.txt', '../hw10_tsp_points_data_0100.txt',
                 '../hw10_tsp_points_data_1000.txt']

    for filename in filenames:
        point_info = read_file(filename)
        labels, points = parse_points(point_info)
        n = len(points)

        nn_tour = nearest_neighbor_tsp(points)

        best_tour, best_distance = parallel_simulated_annealing(points, nn_tour)

        print(f"TSP tour (node order) for {filename}:")
        print(best_tour)
        print(f"Best total distance: {best_distance}")

        plot_tsp(points, best_tour)

if __name__ == "__main__":
    main()