# Computer Vision-Based Harmonic Oscillation Analysis

## Overview

This Python project is designed to analyze the harmonic oscillation of an object using computer vision techniques. It leverages various libraries, including OpenCV for video feed processing, SciPy for data analysis, NumPy for numerical operations, and PyQt5 for creating a graphical user interface (GUI). The project detects and tracks an object in a video feed, extracts its motion data, fits it to a damped oscillation function, and calculates physical parameters such as pendulum length and pivot point location.

[![Harmonic Oscillator Analyzer](https://img.youtube.com/vi/dalsCsHtreU/0.jpg)](https://www.youtube.com/watch?v=dalsCsHtreU&t=1220s)

### Click on the image to watch a review of the project

---

## Read the blog
## It is highly advisable for you, to thoroughly go through the [blog](https://rudrodip.vercel.app/blog/harmonic-oscillation-analyzer). Doing so will greatly facilitate the project setup process and enable a better grasp of the user interface (UI). Your understanding of this section is pivotal in ensuring the efficient configuration of the project and in comprehending the UI.

## Table of Contents

- [Computer Vision-Based Harmonic Oscillation Analysis](#computer-vision-based-harmonic-oscillation-analysis)
  - [Overview](#overview)
    - [Click on the image to watch a review of the project](#click-on-the-image-to-watch-a-review-of-the-project)
  - [Read the blog](#read-the-blog)
  - [It is highly advisable for you, to thoroughly go through the blog. Doing so will greatly facilitate the project setup process and enable a better grasp of the user interface (UI). Your understanding of this section is pivotal in ensuring the efficient configuration of the project and in comprehending the UI.](#it-is-highly-advisable-for-you-to-thoroughly-go-through-the-blog-doing-so-will-greatly-facilitate-the-project-setup-process-and-enable-a-better-grasp-of-the-user-interface-ui-your-understanding-of-this-section-is-pivotal-in-ensuring-the-efficient-configuration-of-the-project-and-in-comprehending-the-ui)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [Usage](#usage)
  - [Object Detection](#object-detection)
  - [Data Collection](#data-collection)
  - [Curve Fitting](#curve-fitting)
    - [Equation for the under-damped oscillation function](#equation-for-the-under-damped-oscillation-function)
    - [Equation for circle residual](#equation-for-circle-residual)
  - [Parameter Estimation](#parameter-estimation)
  - [GUI Integration](#gui-integration)
  - [Visualization](#visualization)
  - [Contributing](#contributing)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).
- [Git](https://git-scm.com/) installed (optional, but recommended for cloning the repository).

## Setting Up a Virtual Environment

It's a good practice to work within a virtual environment to isolate your project's dependencies. Here's how to set up and activate a virtual environment:

1. Open a terminal or command prompt.

2. Clone this repository to your local machine:

```bash
git clone https://github.com/rudrodip/Harmonic-Oscillator-CV
```

3. Navigate to your project directory:

```bash
 cd Harmonic-Oscillator-CV
```

4. Create a virtual environment (replace `venv` with your preferred name):

```bash
  python -m venv venv
```

5. Activate the virtual environment:

  - On Windows:

```bash
  venv\Scripts\activate
```

  - On macOS and Linux:

```bash
  source venv/bin/activate
```

6. Your terminal prompt should now show the name of the virtual environment, indicating that it's active.


## Installing Dependencies

Once you have your virtual environment set up and activated, you can install the project's dependencies:

1. Make sure you are in your project directory with the activated virtual environment.

2. Install the dependencies from the `requirements.txt` file:

```bash
   pip install -r requirements.txt
```

## Usage

1. Run the main application script:

```bash
python app/app.py
```

2. Use the GUI to configure object detection settings and start the analysis.

3. View real-time plots of position vs. time and the fitted damped oscillation function.

4. Extract physical parameters such as pendulum length and pivot point location.

## Object Detection

This project supports multiple object detection methods:

- Color-based masks
- Edge detection
- Hough circles detection

Experiment with these methods and choose the one that works best for your specific application.

## Data Collection

The application captures video frames, detects the object in each frame, and collects position data over time. The data is stored as time vs. x-position pairs in memory.

## Curve Fitting

SciPy's curve fitting functions are used to fit the collected data to a damped oscillation function. This step helps extract parameters like amplitude, frequency, damping coefficient, phase and a constant.

### Equation for the under-damped oscillation function

$$
x(t) = A e^{-\gamma t} \cos(\omega t + \phi) + C
$$

```py
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
```

Equation for decaying oscillation component

$$
x(t) = C \pm A e^{-\gamma t}
$$

```py
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
```

### Equation for circle residual

$$
predicted_y = (x_{\text{rotated}}^2 + y_{\text{rotated}}^2) - r^2
$$

This equation calculates the residuals for fitting a rotated circle to a set of data points, taking into account the transformation of coordinates based on the specified center and rotation.

The rotation of coordinates in the `rotated_circle_residuals` function is based on the following mathematical transformations:

1. If $\theta$ (the angle of rotation) is approximately zero:

$$
\begin{align*}
x_{\text{rotated}} &= x - a \\
y_{\text{rotated}} &= y - b
\end{align*}
$$

2. If $\theta$ is not zero:

$$
\begin{align*}
x_{\text{rotated}} &= (x - a) \cdot \cos(\theta) + (y - b) \cdot \sin(\theta) \\
y_{\text{rotated}} &= (y - b) \cdot \cos(\theta) - (x - a) \cdot \sin(\theta)
\end{align*}
$$

```py
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
```

## Parameter Estimation

The derived parameters are used to estimate other physical properties:

- Pendulum length: Calculated based on the frequency of oscillation.
- Pivot point: Determined using the least squares algorithm.
- Bob radius: Measured from image contours.
- Distance between pivot point and bob surface: Calculated based on bob radius and length of the string.

## GUI Integration

The project features a PyQt5-based GUI that provides a user-friendly interface for configuring the analysis and visualizing the results.

## Visualization

Real-time plots display position vs. time and the fitted damped oscillation function. Additionally, the pendulum string and pivot point are drawn on the video feed.

## Contributing

Contributions to this project are welcome. Feel free to submit bug reports, feature requests, or pull requests to improve the functionality and usability of the application.
