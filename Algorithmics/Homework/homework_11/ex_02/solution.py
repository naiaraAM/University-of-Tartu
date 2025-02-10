import numpy as np
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt

# Generate random coefficients for a 5th-degree polynomial with only three non-zero coefficients
np.random.seed(42)  # Set seed for reproducibility
coefficients = np.zeros(6)
non_zero_indices = np.random.choice(range(6), 3, replace=False)
for idx in non_zero_indices:
    coefficients[idx] = np.round(np.random.uniform(-10, 10), 3)

# Define the original polynomial function
def original_polynomial(x):
    return sum(coefficients[i] * x**i for i in range(6))

# Generate initial random X values within the range -10 to 10
X = np.random.uniform(-10, 10, 100)
Y = np.array([original_polynomial(x) for x in X])

# Calculate maximum absolute value of Y for scaling noise
y_range = np.max(Y) - np.min(Y)
x_range = 20
noise_scale_y = 0.1 * y_range
noise_scale_x = 0.1 * x_range

# Add uniform noise to Y values
noise = np.random.uniform(-noise_scale_y, noise_scale_y, size=Y.shape)
Y_noisy = Y + noise

# Generate additional clusters of random data points centered within a specific region
X_cluster1_center, Y_cluster1_center = 5, noise_scale_y * 5
X_cluster1 = np.random.uniform(X_cluster1_center - noise_scale_x, X_cluster1_center + noise_scale_x, 10)
Y_cluster1 = np.random.uniform(Y_cluster1_center - noise_scale_y, Y_cluster1_center + noise_scale_y, 10)

X_cluster2_center, Y_cluster2_center = -5, -noise_scale_y * 5
X_cluster2 = np.random.uniform(X_cluster2_center - noise_scale_x, X_cluster2_center + noise_scale_x, 10)
Y_cluster2 = np.random.uniform(Y_cluster2_center - noise_scale_y, Y_cluster2_center + noise_scale_y, 10)

# Combine all X and Y data points
X_combined = np.concatenate([X, X_cluster1, X_cluster2])
Y_combined = np.concatenate([Y_noisy, Y_cluster1, Y_cluster2])

# Define the polynomial function to fit
def polynomial(params, x):
    return sum(params[i] * x**i for i in range(6))

# Define the MSE function
def mse(params):
    return np.mean((Y_combined - polynomial(params, X_combined)) ** 2)

# Define the MedSE function
def medse(params):
    return np.median((Y_combined - polynomial(params, X_combined)) ** 2)

# Define the bounds for the coefficients
bounds = [(-10, 10)] * 6

# Perform differential evolution for MSE
result_de_mse = differential_evolution(mse, bounds)
best_params_mse = result_de_mse.x

# Perform differential evolution for MedSE
result_de_medse = differential_evolution(medse, bounds)
best_params_medse = result_de_medse.x

# Define functions for each fitted polynomial
def fitted_polynomial_mse(x):
    return polynomial(best_params_mse, x)

def fitted_polynomial_medse(x):
    return polynomial(best_params_medse, x)

# Plot settings
plt.figure(figsize=(10, 6))
plt.scatter(X_combined, Y_combined, color="blue", s=20, label="Noisy Data Points")
plt.plot(np.sort(X_combined), original_polynomial(np.sort(X_combined)), color="blue", linestyle="--", label="Original True Polynomial")
plt.plot(np.sort(X_combined), fitted_polynomial_mse(np.sort(X_combined)), color="pink", label="DE MSE Fit")
plt.plot(np.sort(X_combined), fitted_polynomial_medse(np.sort(X_combined)), color="red", label="DE MedSE Fit")

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Scatter Plot with Polynomial Fits using Differential Evolution")
plt.legend()
plt.show()

# Print the coefficients for reference
print("Original random 5th-degree polynomial coefficients:\n", coefficients)
print("Fitted 5th-degree polynomial coefficients (MSE):\n", [f"{coef:.3f}" for coef in best_params_mse])
print("Fitted 5th-degree polynomial coefficients (MedSE):\n", [f"{coef:.3f}" for coef in best_params_medse])