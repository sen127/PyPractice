import matplotlib.pyplot as plt
import numpy as np

# Data
miles_list_atc = [1874, 492, 2294, 313, 2706, 3425, 3255, 7883, 6552, 6438]
atc_costs = [371.80, 97.61, 455.13, 62.10, 536.87, 679.52, 645.79, 1563.99, 1299.92, 1277.30]

# Fit a polynomial curve (quadratic fit)
coefficients = np.polyfit(miles_list_atc, atc_costs, 2)
polynomial = np.poly1d(coefficients)

# Generate smooth data points for the curve
x_smooth = np.linspace(min(miles_list_atc), max(miles_list_atc), 500)
y_smooth = polynomial(x_smooth)

# Plot the data and smoothed curve
plt.figure(figsize=(10, 6))
plt.scatter(miles_list_atc, atc_costs, color='blue', label='Original Data')  # Original data points
plt.plot(x_smooth, y_smooth, color='green', label='Smoothed Curve')  # Smoothed curve
plt.title("ATC (Average Total Cost) vs. Distance")
plt.xlabel("Distance (Miles)")
plt.ylabel("ATC (CAD)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()