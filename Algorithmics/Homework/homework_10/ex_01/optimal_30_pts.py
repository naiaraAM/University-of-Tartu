import os
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def read_file(file_path):
    points = []
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]  # Skip metadata
        for line in lines:
            point_id, x, y = line.strip().split()
            points.append((point_id, int(x), int(y)))
    return points

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '../hw10_tsp_points_data_0030.txt')

point_info = read_file(file_path)

steps = []

def nearest_neighbour(points):
    path = [points[0]]
    points = points[1:]
    while points:
        nearest_point = min(points, key=lambda x: (x[1] - path[-1][1]) ** 2 + (x[2] - path[-1][2]) ** 2)
        path.append(nearest_point)
        points.remove(nearest_point)
        steps.append(('Nearest Neighbour Path Step', list(path)))
    return path

def calculate_path_length(path):
    return sum(math.dist(path[i][1:], path[i + 1][1:]) for i in range(len(path) - 1)) + math.dist(path[-1][1:], path[0][1:])

def two_opt(path):
    best_path = path
    best_length = calculate_path_length(path)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1: continue
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                new_length = calculate_path_length(new_path)
                if new_length < best_length:
                    best_path = new_path
                    best_length = new_length
                    improved = True
                    steps.append(('2-opt Optimization Step', list(best_path)))
        path = best_path
    return best_path

def plot_path_step(points, path, title):
    plt.clf()
    plt.scatter([p[1] for p in points], [p[2] for p in points], c='blue')
    for i in range(len(path) - 1):
        plt.plot([path[i][1], path[i + 1][1]], [path[i][2], path[i + 1][2]], 'k-')
    plt.plot([path[-1][1], path[0][1]], [path[-1][2], path[0][2]], 'k-')
    plt.title(title)

initial_path = nearest_neighbour(point_info)

optimized_path = two_opt(initial_path)

# Create animation
fig = plt.figure()

def animate(i):
    title, path = steps[i]
    plot_path_step(point_info, path, title)

ani = animation.FuncAnimation(fig, animate, frames=len(steps), interval=500, repeat=True)
ani.save('tsp_optimization.gif', writer='imagemagick')

print("Initial path length:", calculate_path_length(initial_path))
print("Optimized path length:", calculate_path_length(optimized_path))

# for the optimized path, just print the points id
print("Optimized path:", [p[0] for p in optimized_path])
