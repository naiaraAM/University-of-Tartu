import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Define the functions
def quadratic(x):
    return a * x**2 + b * x + c

def rosenbrock(x):
    a, b = 1, 100
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def negative_sine(x):
    return -np.sin(x)

def complex_polynomial(x):
    return 10 + 10 * abs(np.sin(x) * sum(c * x**i for i, c in enumerate(coefficients)))

# Generate random coefficients for the quadratic function
a = np.round(np.random.uniform(2, 10), 3)
b = np.round(np.random.uniform(-10, 10), 3)
c = np.round(np.random.uniform(-10, 10), 3)

# Generate random coefficients for an 8th-degree polynomial
coefficients = np.random.uniform(-10, 10, 5)

# Define the Differential Evolution algorithm
def differential_evolution(func, bounds, max_iter=1000, pop_size=50, mutation=0.5, recombination=0.7):
    dimensions = len(bounds)
    pop = np.random.rand(pop_size, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([func(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]

    for i in range(max_iter):
        for j in range(pop_size):
            idxs = [idx for idx in range(pop_size) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            mutant = np.clip(a + mutation * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < recombination
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = func(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]

# Define bounds for each function
bounds_quadratic = [(-10, 10)]
bounds_rosenbrock = [(-2, 2), (-1, 3)]
bounds_sine = [(0, 2 * np.pi)]
bounds_complex_polynomial = [(-5, 5)]

# Run Differential Evolution for each function
result_de_quadratic = list(differential_evolution(quadratic, bounds_quadratic))[-1]
result_de_rosenbrock = list(differential_evolution(rosenbrock, bounds_rosenbrock))[-1]
result_de_sine = list(differential_evolution(negative_sine, bounds_sine))[-1]
result_de_complex_polynomial = list(differential_evolution(complex_polynomial, bounds_complex_polynomial))[-1]

# Perform minimization using scipy.optimize.minimize
result_quadratic = minimize(quadratic, x0=0)
result_rosenbrock = minimize(rosenbrock, x0=[0, 0])
result_sine = minimize(negative_sine, x0=2)

# Use multiple starting points to try to find a global minimum for the complex polynomial
starting_points = np.linspace(-5, 5, 10)
best_result_complex_polynomial = None
for start in starting_points:
    result = minimize(complex_polynomial, x0=start)
    if best_result_complex_polynomial is None or result.fun < best_result_complex_polynomial.fun:
        best_result_complex_polynomial = result

# Generate data for plotting
x_vals_quadratic = np.linspace(-10, 10, 200)
y_vals_quadratic = quadratic(x_vals_quadratic)

x_vals_rosenbrock = np.linspace(-2, 2, 100)
y_vals_rosenbrock = np.linspace(-1, 3, 100)
X_rosenbrock, Y_rosenbrock = np.meshgrid(x_vals_rosenbrock, y_vals_rosenbrock)
Z_rosenbrock = rosenbrock([X_rosenbrock, Y_rosenbrock])

x_vals_sine = np.linspace(0, 2 * np.pi, 100)
y_vals_sine = np.sin(x_vals_sine)

x_vals_complex_polynomial = np.linspace(-5, 5, 400)
y_vals_complex_polynomial = [complex_polynomial(x) for x in x_vals_complex_polynomial]

# Visualization for quadratic function
plt.figure()
plt.plot(x_vals_quadratic, y_vals_quadratic, label=f"f(x) = {a}x^2 + {b}x + {c}")
plt.scatter(result_quadratic.x, result_quadratic.fun, color="red", label="Scipy Minimum", zorder=5, s=100)
plt.scatter(result_de_quadratic[0], result_de_quadratic[1], color="green", label="DE Minimum", zorder=6, s=100)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Random Quadratic Function Minimization")
plt.legend()
plt.show()

# Visualization for Rosenbrock function
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_rosenbrock, Y_rosenbrock, Z_rosenbrock, cmap="viridis", alpha=0.6)
ax.scatter(result_rosenbrock.x[0], result_rosenbrock.x[1], result_rosenbrock.fun, color="red", label="Scipy Minimum", s=100)
ax.scatter(result_de_rosenbrock[0][0], result_de_rosenbrock[0][1], result_de_rosenbrock[1], color="green", label="DE Minimum", s=100)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
plt.title("Rosenbrock Function Minimization")
plt.legend()
plt.show()

# Visualization for sine function
plt.figure()
plt.plot(x_vals_sine, y_vals_sine, label="f(x) = sin(x)")
plt.scatter(result_sine.x, -result_sine.fun, color="red", label="Scipy Maximum", zorder=5, s=100)
plt.scatter(result_de_sine[0], -result_de_sine[1], color="green", label="DE Maximum", zorder=6, s=100)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Sine Function Maximization")
plt.legend()
plt.show()

# Visualization for complex polynomial function
plt.figure()
plt.plot(x_vals_complex_polynomial, y_vals_complex_polynomial, label="8th-degree polynomial (absolute value)")
plt.scatter(best_result_complex_polynomial.x, best_result_complex_polynomial.fun, color="red", label="Scipy Minimum", zorder=5, s=5)
plt.scatter(result_de_complex_polynomial[0], result_de_complex_polynomial[1], color="green", label="DE Minimum", zorder=6, s=5)
plt.xlabel("x")
plt.ylabel("|f(x)|")
plt.yscale("log")
plt.title("Optimization of a Random 8th-Degree Polynomial Function (Log Scale, Absolute Value)")
plt.legend()
plt.show()

def percentage_difference(val1, val2):
    return np.abs(val1 - val2)

data = {
    "Function": ["Quadratic", "Rosenbrock", "Sine", "Complex Polynomial"],
    "Scipy Min/Max": [
        result_quadratic.fun,
        result_rosenbrock.fun,
        -result_sine.fun,
        best_result_complex_polynomial.fun,
    ],
    "DE Min/Max": [
        result_de_quadratic[1],
        result_de_rosenbrock[1],
        -result_de_sine[1],
        result_de_complex_polynomial[1],
    ],
    "Difference": [
        result_de_quadratic[1] - result_quadratic.fun,
        result_de_rosenbrock[1] - result_rosenbrock.fun,
        -result_de_sine[1] - (-result_sine.fun),
        result_de_complex_polynomial[1] - best_result_complex_polynomial.fun,
    ],
}
# data to MD table
df = pd.DataFrame(data)

df["Difference"] = df["Difference"].round(8)

print(df.to_markdown())