import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Generate random coefficients for the quadratic function with 3 decimal places
a = np.round(np.random.uniform( 2 , 10), 3)
b = np.round(np.random.uniform(-10, 10), 3)
c = np.round(np.random.uniform(-10, 10), 3)

# Define the function using the generated coefficients
def quadratic(x):
    return a * x**2 + b * x + c

# Perform minimization
result = minimize(quadratic, x0=0)

# Generate data for plotting
x_vals = np.linspace(-10, 10, 200)
y_vals = quadratic(x_vals)

# Plot
plt.figure()
plt.plot(x_vals, y_vals, label=f"f(x) = {a}x^2 + {b}x + {c}")
plt.scatter(result.x, result.fun, color="red", label="Minimum", zorder=5)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Random Quadratic Function Minimization")
plt.legend()
plt.show()

# Print the result
print("Random coefficients: a =", a, ", b =", b, ", c =", c)
print("Best Minimum Found:", result.x, "with function value:", result.fun)

from mpl_toolkits.mplot3d import Axes3D

# Define the Rosenbrock function
def rosenbrock(x):
    a, b = 1, 100
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

# Perform minimization
result = minimize(rosenbrock, x0=[0, 0])

# Generate data for plotting
x_vals = np.linspace(-2, 2, 100)
y_vals = np.linspace(-1, 3, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = rosenbrock([X, Y])

# Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.6)
ax.scatter(result.x[0], result.x[1], result.fun, color="red", label="Minimum", s=50)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
plt.title("Rosenbrock Function Minimization")
plt.legend()
plt.show()

# Define the sine function for maximization
def negative_sine(x):
    return -np.sin(x)

# Perform minimization to find the maximum of sine
result = minimize(negative_sine, x0=2)

# Generate data for plotting
x_vals = np.linspace(0, 2 * np.pi, 100)
y_vals = np.sin(x_vals)

# Plot
plt.figure()
plt.plot(x_vals, y_vals, label="f(x) = sin(x)")
plt.scatter(result.x, -result.fun, color="red", label="Maximum", zorder=5)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Sine Function Maximization")
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Generate random coefficients for an 8th-degree polynomial
coefficients = np.random.uniform(-10, 10, 5)  # Random coefficients between -10 and 10

# Define the polynomial function with absolute values
def complex_polynomial(x):
    return 10+ 10*abs( np.sin(x) * sum(c * x**i for i, c in enumerate(coefficients)))

# Use multiple starting points to try to find a global minimum
starting_points = np.linspace(-5, 5, 10)
best_result = None
for start in starting_points:
    result = minimize(complex_polynomial, x0=start)
    if best_result is None or result.fun < best_result.fun:
        best_result = result

# Generate data for plotting
x_vals = np.linspace(-5, 5, 400)
y_vals = [complex_polynomial(x) for x in x_vals]

# Plot the function as a line
plt.figure()
plt.plot(x_vals, y_vals, label="8th-degree polynomial (absolute value)")
plt.scatter(best_result.x, best_result.fun, color="red", label="Minimum", zorder=5)
plt.xlabel("x")
plt.ylabel("|f(x)|")
plt.yscale("log")  # Set y-axis to logarithmic scale
plt.title("Optimization of a Random 8th-Degree Polynomial Function (Log Scale, Absolute Value)")
plt.legend()
plt.show()

print("Best Minimum Found:", best_result.x, "with function value:", best_result.fun)

