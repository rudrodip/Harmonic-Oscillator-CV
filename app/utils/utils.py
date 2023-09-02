import json
import numpy as np

# Function to load JSON data from a file
def load_json(filename):
    try:
        with open(filename, "r") as f:
            hsv = json.load(f)
            return hsv
    except:
        print(f'Cannot load {filename}. Returning blank value.')
        return { }

# Function to save JSON data to a file
def save_json(filename, jsonfile):
    with open(filename, "w") as f:
        json.dump(jsonfile, f)

    print(f'Saved {filename}')

# Function to model an underdamped harmonic oscillator
def underdamped_harmonic_oscillator(t, A, gamma, f, phi, C):
    """
    Calculate the position of an underdamped harmonic oscillator at time t.

    Args:
        t: Time values.
        A: Amplitude of oscillation.
        gamma: Damping coefficient.
        f: Frequency of oscillation.
        phi: Phase angle.
        C: Constant offset.

    Returns:
        Position values at the given time points.
    """
    return A * np.exp(-gamma * t) * np.cos(2 * np.pi * f * t + phi) + C

# Function to model the upper decaying component of a curve
def upper_decaying_component_curve(t, A, gamma, C):
    """
    Calculate the upper decaying component of a curve at time t.

    Args:
        t: Time values.
        A: Amplitude of decay.
        gamma: Decay rate.
        C: Constant offset.

    Returns:
        Value of the upper decaying component at the given time points.
    """
    return C + A * np.exp(-gamma * t)

# Function to model the lower decaying component of a curve
def lower_decaying_component_curve(t, A, gamma, C):
    """
    Calculate the lower decaying component of a curve at time t.

    Args:
        t: Time values.
        A: Amplitude of decay.
        gamma: Decay rate.
        C: Constant offset.

    Returns:
        Value of the lower decaying component at the given time points.
    """
    return C - A * np.exp(-gamma * t)

# Function to calculate residuals for circle fitting
def circle_residuals(params, x, y):
    """
    Calculate the residuals for circle fitting.

    Args:
        params: Parameters of the circle (a, b, r).
        x: x-coordinates of data points.
        y: y-coordinates of data points.

    Returns:
        Residuals indicating the difference between the data points and the circle model.
    """
    a, b, r = params
    return np.sqrt((x - a) ** 2 + (y - b) ** 2) - r
