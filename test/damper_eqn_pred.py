import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from app.utils.utils import get_project_root, underdamped_harmonic_oscillator
from app.utils.contansts import initial_guess, lower_bounds, upper_bounds

project_root = get_project_root(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(project_root, 'data')

# Read the CSV file
data_points = []
with open(os.path.join(data_folder, "csv", "transformed_data.csv"), 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        cx, _, time = map(float, row)
        data_points.append((time, cx))

times, cx_values = zip(*data_points)

# Convert the data to NumPy arrays
times = np.array(times)
cx_values = np.array(cx_values)

# Perform the curve fitting
params, params_covariance = curve_fit(underdamped_harmonic_oscillator, times, cx_values, p0=initial_guess, bounds=(lower_bounds, upper_bounds))

# Extract the fitted parameters
A, gamma, w, phi, C = params

print("Fitted Parameters:")
print("Amplitude (A):", A)
print("Damping Coefficient (gamma):", gamma)
print("Omega (f):", w)
print("Phase (phi):", phi)
print("Vertical Offset (C):", C)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(times, cx_values, label='Data', marker='o')
plt.plot(times, underdamped_harmonic_oscillator(times, A, gamma, w, phi, C), label='Fitted Damped Harmonic Oscillator', linestyle='--')
plt.xlabel('Time (seconds)')
plt.ylabel('X Position')
plt.title('Fitted Damped Harmonic Oscillator')
plt.legend()
plt.grid(True)
plt.show()
