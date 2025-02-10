import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Set the random seed for reproducibility (optional)
np.random.seed(42)  # You can insert your own seed for reproducibility

# Generate random coefficients for a 5th-degree polynomial with only three non-zero coefficients
coefficients = np.zeros(6)
non_zero_indices = np.random.choice(range(6), 3, replace=False)  # Randomly pick 3 indices to be non-zero
for idx in non_zero_indices:
    coefficients[idx] = np.round(np.random.uniform(-10, 10), 3)  # Limit each coefficient to 3 decimal places

# Define the original polynomial function
def original_polynomial(x):
    return sum(coefficients[i] * x**i for i in range(6))

# Generate initial random X values within the range -10 to 10
X = np.random.uniform(-10, 10, 100)
Y = np.array([original_polynomial(x) for x in X])

# Calculate maximum absolute value of Y for scaling noise
y_range = np.max(Y) - np.min(Y)
x_range = 20  # Range of X values (-10 to 10)
noise_scale_y = 0.1 * y_range  # 10% of the Y range for Y noise
noise_scale_x = 0.1 * x_range  # 10% of the X range for X noise

# Add uniform noise to Y values
noise = np.random.uniform(-noise_scale_y, noise_scale_y, size=Y.shape)
Y_noisy = Y + noise

# Generate additional clusters of random data points centered within a specific region
# Cluster 1: centered around X=5, Y=10, with 10% spread in both X and Y
X_cluster1_center, Y_cluster1_center = 5, noise_scale_y*5
X_cluster1 = np.random.uniform(X_cluster1_center - noise_scale_x, X_cluster1_center + noise_scale_x, 10)
Y_cluster1 = np.random.uniform(Y_cluster1_center - noise_scale_y, Y_cluster1_center + noise_scale_y, 10)

# Cluster 2: centered around X=-5, Y=-10, with 10% spread in both X and Y
X_cluster2_center, Y_cluster2_center = -5, -noise_scale_y*5
X_cluster2 = np.random.uniform(X_cluster2_center - noise_scale_x, X_cluster2_center + noise_scale_x, 10)
Y_cluster2 = np.random.uniform(Y_cluster2_center - noise_scale_y, Y_cluster2_center + noise_scale_y, 10)

# Combine all X and Y data points
X_combined = np.concatenate([X, X_cluster1, X_cluster2])
Y_combined = np.concatenate([Y_noisy, Y_cluster1, Y_cluster2])

# Fit a 5th-degree polynomial to the combined noisy data
poly_fit = np.polyfit(X_combined, Y_combined, 5)
poly_fit_fn = np.poly1d(poly_fit)  # Convert to a polynomial function for easy evaluation

# Print the polynomial as text with largest degrees first
poly_text = " + ".join([f"{coef:.3f} * x^{5 - i}" for i, coef in enumerate(poly_fit)])
print(f"Fitted 5th-degree polynomial: \nf(x) = {poly_text}")

# Calculate the MSE for the fitted polynomial
Y_pred_poly = poly_fit_fn(X_combined)
mse_poly = np.mean((Y_combined - Y_pred_poly) ** 2)
print(f"Mean Squared Error (MSE) of fitted polynomial: {mse_poly}")

# Calculate the Median Squared Error (MedSE) for the fitted polynomial
medse_poly = np.median((Y_combined - Y_pred_poly) ** 2)
print(f"Median Squared Error (MedSE) of fitted polynomial: {medse_poly}")

# Fit the linear regression using Mean Squared Error (MSE)
slope_mse, intercept_mse = np.polyfit(X_combined, Y_combined, 1)

# Define the function for Median Squared Error (MSE)
def median_squared_error(params, X, Y):
    slope, intercept = params
    Y_pred = slope * X + intercept
    return np.median((Y - Y_pred) ** 2)

# Fit the linear regression using Median Squared Error
initial_guess = [0, 0]
result_median = minimize(median_squared_error, initial_guess, args=(X_combined, Y_combined))
slope_median, intercept_median = result_median.x

# Define functions for each fitted line
def mse_line(x):
    return slope_mse * x + intercept_mse

def median_line(x):
    return slope_median * x + intercept_median

# Plot settings
plt.figure(figsize=(10, 6))  # Increase figure size
plt.scatter(X, Y_noisy, color="blue", s=20, label="Noisy Data Points")  # Original noisy data points
plt.scatter(X_cluster1, Y_cluster1, color="purple", s=20, label="Cluster 1 Data Points")
plt.scatter(X_cluster2, Y_cluster2, color="green", s=20, label="Cluster 2 Data Points")

# Plot the original "true" polynomial function used to generate the data
plt.plot(np.sort(X_combined), original_polynomial(np.sort(X_combined)), color="blue", linestyle="--", label="Original True Polynomial")

# Plot fitted polynomial and linear regression lines
plt.plot(np.sort(X_combined), poly_fit_fn(np.sort(X_combined)), color="pink", label="5th-degree Polynomial Fit")  # Polynomial trendline
plt.plot(np.sort(X_combined), mse_line(np.sort(X_combined)), color="lightblue", label="Linear MSE Fit")  # Linear MSE trendline
plt.plot(np.sort(X_combined), median_line(np.sort(X_combined)), color="lightgreen", label="Linear Median Squared Error Fit")  # Linear Median trendline

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Scatter Plot with Polynomial and Linear Regression Trendlines (with Additional Clusters)")
plt.legend()
plt.show()

# Print the polynomial, MSE, and median coefficients for reference
print("Original random 5th-degree polynomial coefficients:\n", coefficients)
print("Polynomial function: f(x) = ", " + ".join([f"{coeff}*x^{i}" for i, coeff in reversed(list(enumerate(coefficients))) if coeff != 0]))
print("Fitted 5th-degree polynomial coefficients:\n", [f"{coef:.3f}" for coef in poly_fit])

# Print the linear regression coefficients for both MSE and Median Squared Error
print("\nLinear MSE Regression coefficients (slope and intercept):")
print("Slope:", slope_mse)
print("Intercept:", intercept_mse)

print("\nLinear Median Squared Error Regression coefficients (slope and intercept):")
print("Slope:", slope_median)
print("Intercept:", intercept_median)
