import numpy as np
import matplotlib.pyplot as plt
import time
import random
import os

def read_cities(file_path):
    cities = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):  # Skip comment lines
                continue
            parts = line.strip().split()
            city_name = parts[0]
            x_coord = float(parts[1])
            y_coord = float(parts[2])
            cities.append((city_name, x_coord, y_coord))
    return cities

def distance_matrix(cities):
    num_cities = len(cities)
    dist = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            x1, y1 = cities[i][1], cities[i][2]
            x2, y2 = cities[j][1], cities[j][2]
            dist[i][j] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def total_distance(tour, dist_matrix):
    return sum(dist_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + dist_matrix[tour[-1], tour[0]]

def nearest_neighbour_solution(dist_matrix):
    num_cities = len(dist_matrix)
    visited = [0]
    while len(visited) < num_cities:
        last = visited[-1]
        next_city = np.argmin([dist_matrix[last, j] if j not in visited else np.inf for j in range(num_cities)])
        visited.append(next_city)
    return visited

def simulated_annealing(dist_matrix, initial_tour, initial_temp=1000, alpha=0.995, max_iter=1000):
    num_cities = len(dist_matrix)
    current_tour = initial_tour[:]
    current_distance = total_distance(current_tour, dist_matrix)
    best_tour = current_tour[:]
    best_distance = current_distance

    temperature = initial_temp
    start_time = time.time()

    for _ in range(max_iter):
        for _ in range(num_cities):
            i, j = random.sample(range(num_cities), 2)
            new_tour = current_tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_distance = total_distance(new_tour, dist_matrix)

            delta = new_distance - current_distance
            if delta < 0 or random.random() < np.exp(-delta / temperature):
                current_tour = new_tour
                current_distance = new_distance
                if new_distance < best_distance:
                    best_tour = new_tour[:]
                    best_distance = new_distance

        # Cool down
        temperature *= alpha
        if temperature < 1e-3:
            break

    compute_time = time.time() - start_time
    return best_tour, best_distance, compute_time

def plot_tour(cities, tour, title, file_name):
    tour_coords = np.array([cities[i][1:] for i in tour + [tour[0]]])  # Get coordinates of the tour
    plt.figure(figsize=(8, 8))
    plt.plot(tour_coords[:, 0], tour_coords[:, 1], marker='.', linestyle='-', color='blue')
    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.savefig(file_name)
    plt.close()

file_paths = ['../hw10_tsp_points_data_0030.txt', '../hw10_tsp_points_data_0100.txt', '../hw10_tsp_points_data_0200.txt', '../hw10_tsp_points_data_1000.txt']
for file in file_paths:
    cities = read_cities(file)
    dist_matrix = distance_matrix(cities)

    random_tour = list(range(len(cities)))
    random.shuffle(random_tour)
    sa_random_tour, sa_random_distance, random_time = simulated_annealing(dist_matrix, random_tour)

    start_nn_time = time.time()
    nn_tour = nearest_neighbour_solution(dist_matrix)
    nn_distance = total_distance(nn_tour, dist_matrix)
    nn_time = time.time() - start_nn_time

    sa_nn_tour, sa_nn_distance, sa_nn_time = simulated_annealing(dist_matrix, nn_tour)

    # Plot and Compare
    print("Starting from Random:")
    print(f"Distance: {sa_random_distance:.2f}, Time: {random_time:.2f} seconds")
    plot_tour(cities, sa_random_tour, "SA Solution (Random)", f"sa_random_{os.path.basename(file)}.png")

    print("Starting from NN:")
    print(f"NN Distance: {nn_distance:.2f}, NN Time: {nn_time:.2f} seconds")
    print(f"SA Distance: {sa_nn_distance:.2f}, SA Time: {sa_nn_time:.2f} seconds")
    plot_tour(cities, nn_tour, "NN Solution", f"nn_{os.path.basename(file)}.png")
    plot_tour(cities, sa_nn_tour, "SA Solution (NN)", f"sa_nn_{os.path.basename(file)}.png")