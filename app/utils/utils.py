import os
import json
import numpy as np

# Function to load JSON data from a file
def load_json(filename):
    try:
        with open(filename, "r") as f:
            hsv = json.load(f)
            return hsv
    except Exception as e:
        print(e)

# Function to save JSON data to a file
def save_json(filename, jsonfile):
    with open(filename, "w") as f:
        json.dump(jsonfile, f)

    print(f'Saved {filename}')

def get_project_root(start_directory):
    current_directory = start_directory

    # Search for the marker file (.project_root) or a specific folder (e.g., 'src')
    while True:
        if os.path.exists(os.path.join(current_directory, 'setup.py')):
            return current_directory

        current_directory = os.path.dirname(current_directory)

        # Break if we have reached the root directory
        if current_directory == start_directory or current_directory == os.path.dirname(current_directory):
            break
    return ''

# Function to model an underdamped harmonic oscillator
def underdamped_harmonic_oscillator(t, A, gamma, w, phi, C):
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
    return A * np.exp(-gamma * t) * np.cos(w * t + phi) + C

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

# Calculate the residuals for fitting a rotated circle to data points
def rotated_circle_residuals(params, x, y):
    """
    Parameters:
        params (list): A list containing the parameters of the rotated circle.
            params[0] (float): 'a' - X-coordinate of the circle's center.
            params[1] (float): 'b' - Y-coordinate of the circle's center.
            params[2] (float): 'r' - Radius of the circle.
            params[3] (float): 'theta' - Angle of rotation of the circle (in radians).
        x (array): Array containing the x-coordinates of data points.
        y (array): Array containing the y-coordinates of data points.

    Returns:
        predicted_y (array): Array of residuals, i.e., the differences between
        the observed data points and the corresponding points on the rotated circle.

    Notes:
        This function calculates the residuals for fitting a rotated circle to a set of data points.
        It transforms the data points based on the specified center ('a', 'b') and rotation ('theta')
        and computes the differences between the observed 'y' values and the predicted 'y' values
        on the rotated circle.
    """
    a, b, r, theta = params  # Extract the parameters

    if np.isclose(theta, 0, atol=1e-6):
        x_rotated = x - a
        y_rotated = y - b
    else:
        x_rotated = (x - a) * np.cos(theta) + (y - b) * np.sin(theta)
        y_rotated = (y - b) * np.cos(theta) - (x - a) * np.sin(theta)

    predicted_y = x_rotated**2 + y_rotated**2 - r**2  # Calculate residuals based on the rotated circle
    return predicted_y


def rotation_matrix(angle_radians):
    """
    Generate a 2D rotation matrix for a given angle in radians.
    """
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)
    
    return np.array([[cos_theta, -sin_theta],
                    [sin_theta, cos_theta]])

# Rotate a point (x, y) around a pivot point (pivot_x, pivot_y) by a specified angle in radians
def rotate_point(x, y, pivot_x, pivot_y, angle_radians):
    '''
    Rotate a point (x, y) around a pivot point (pivot_x, pivot_y) by a specified angle in radians.

    Parameters:
        x (float): X-coordinate of the point to be rotated.
        y (float): Y-coordinate of the point to be rotated.
        pivot_x (float): X-coordinate of the pivot point.
        pivot_y (float): Y-coordinate of the pivot point.
        angle_radians (float): Angle of rotation in radians.

    Returns:
        Tuple[float, float]: Transformed coordinates (x_transformed, y_transformed).
    '''

    # Calculate relative coordinates
    relative_x = x - pivot_x
    relative_y = y - pivot_y

    # Create a rotation matrix
    rotation_matrix_2d = rotation_matrix(angle_radians)

    # Apply rotation matrix
    rotated = np.dot(rotation_matrix_2d, [relative_x, relative_y])

    # Calculate transformed coordinates
    x_transformed = pivot_x + rotated[0]
    y_transformed = pivot_y + rotated[1]

    # Return transformed coordinates
    return x_transformed, y_transformed

import numpy as np

def rotate_opencv_point(x, y, pivot_x, pivot_y, angle_radians, window_height):
    '''
    Rotate a point (x, y) in an OpenCV-like coordinate system around a pivot point (pivot_x, pivot_y)
    by a specified angle in radians.

    Parameters:
        x (float): X-coordinate of the point to be rotated.
        y (float): Y-coordinate of the point to be rotated.
        pivot_x (float): X-coordinate of the pivot point.
        pivot_y (float): Y-coordinate of the pivot point.
        angle_radians (float): Angle of rotation in radians.
        window_height (int): Height of the OpenCV-like window (used to adjust the y-coordinate).

    Returns:
        Tuple[float, float]: Transformed coordinates (x_transformed, y_transformed).
    '''

    # Adjust the pivot point's y-coordinate to match the top-left origin
    pivot_y = window_height - pivot_y

    # Reverse the sign of the angle for clockwise rotation (if necessary)
    # If you're working in a counterclockwise rotation system, you can skip this step
    angle_radians = -angle_radians

    # Calculate relative coordinates
    relative_x = x - pivot_x
    relative_y = y - pivot_y

    # Calculate the sine and cosine of the angle
    cos_theta = np.cos(angle_radians)
    sin_theta = np.sin(angle_radians)

    # Apply rotation matrix
    x_transformed = pivot_x + (relative_x * cos_theta - relative_y * sin_theta)
    y_transformed = pivot_y + (relative_x * sin_theta + relative_y * cos_theta)

    # Adjust the y-coordinate back to the original coordinate system
    y_transformed = window_height - y_transformed

    # Return transformed coordinates
    return x_transformed, y_transformed

def opencv_to_cartesian(opencv_coords, frame_height):
    """
    Convert coordinates from OpenCV coordinate system to Cartesian coordinate system.

    Parameters:
        opencv_coords (tuple): A tuple containing the (x, y) coordinates in OpenCV coordinate system.
        frame_height (int): The height (number of rows) of the image.

    Returns:
        tuple: A tuple containing the corresponding (x, y) coordinates in Cartesian coordinate system.

    Notes:
        In OpenCV coordinate system, the origin (0,0) is at the top-left corner of the image.
        In Cartesian coordinate system, the origin (0,0) is at the bottom-left corner of the image.

        This function converts OpenCV coordinates to Cartesian coordinates using the formula:
        x_cartesian = x_opencv
        y_cartesian = frame_height - y_opencv
    """
    x_opencv, y_opencv = opencv_coords
    x_cartesian = x_opencv
    y_cartesian = frame_height - y_opencv
    return x_cartesian, y_cartesian
