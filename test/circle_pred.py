import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from app.utils.utils import rotated_circle_residuals, get_project_root

project_root = get_project_root(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, 'data')

# Define the rotated circle function
def rotated_circle(theta, a, b, r):
    x = a + r * np.cos(theta)
    y = b + r * np.sin(theta)
    return x, y

# Read the CSV file
data_points = []
with open(os.path.join(data_folder, "csv", "transformed_data.csv"), 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        cx, cy, time = map(float, row)
        data_points.append((cx, cy))

cx, cy = zip(*data_points)

# Convert the data to NumPy arrays
cx = np.array(cx)
cy = np.array(cy)

# Initial guesses for the parameters
initial_guess = [0.0, 0.0, 1.0, 0.0]

# Perform the least squares fitting
circle_result = least_squares(rotated_circle_residuals, initial_guess, args=(cx, cy))

# Extract the fitted parameters including theta
fitted_a, fitted_b, fitted_r, fitted_theta = circle_result.x

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the original data points (cx, cy)
plt.plot(cx, cy, label='Data', marker='o', linestyle='None', markersize=5, color='blue')

for param in circle_result.x:
    print(param)

# Plot the fitted rotated circle
fitted_theta_range = np.linspace(0, 2 * np.pi, 100)
fitted_x, fitted_y = rotated_circle(fitted_theta_range, fitted_a, fitted_b, fitted_r)
plt.plot(fitted_x, fitted_y, label='Fitted Rotated Circle', color='red')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Fitted Rotated Circle and Custom (cx, cy) Values')
plt.legend()
plt.grid(True)
plt.axis('equal')  # Make the aspect ratio of the plot equal
plt.show()
