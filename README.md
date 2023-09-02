# Computer Vision-Based Harmonic Oscillation Analysis

## Overview

This Python project is designed to analyze the harmonic oscillation of an object using computer vision techniques. It leverages various libraries, including OpenCV for video feed processing, SciPy for data analysis, NumPy for numerical operations, and PyQt5 for creating a graphical user interface (GUI). The project detects and tracks an object in a video feed, extracts its motion data, fits it to a damped oscillation function, and calculates physical parameters such as pendulum length and pivot point location.

## Table of Contents

- [Computer Vision-Based Harmonic Oscillation Analysis](#computer-vision-based-harmonic-oscillation-analysis)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
  - [Usage](#usage)
  - [Object Detection](#object-detection)
  - [Data Collection](#data-collection)
  - [Curve Fitting](#curve-fitting)
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

Equation for the under-damped oscillation function

$$
x(t) = A e^{-\gamma t} \cos(2\pi f t + \phi) + C
$$

```py
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

Equation for circle residual

$$
\sqrt{(x - a)^2 + (y - b)^2} - r
$$

```py
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