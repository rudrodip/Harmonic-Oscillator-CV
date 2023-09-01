# Computer Vision-Based Harmonic Oscillation Analysis

## Overview

This Python project is designed to analyze the harmonic oscillation of an object using computer vision techniques. It leverages various libraries, including OpenCV for video feed processing, SciPy for data analysis, NumPy for numerical operations, and PyQt5 for creating a graphical user interface (GUI). The project detects and tracks an object in a video feed, extracts its motion data, fits it to a damped oscillation function, and calculates physical parameters such as pendulum length and pivot point location.

## Table of Contents

- [Computer Vision-Based Harmonic Oscillation Analysis](#computer-vision-based-harmonic-oscillation-analysis)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Object Detection](#object-detection)
  - [Data Collection](#data-collection)
  - [Curve Fitting](#curve-fitting)
  - [Parameter Estimation](#parameter-estimation)
  - [GUI Integration](#gui-integration)
  - [Visualization](#visualization)
  - [Contributing](#contributing)

## Prerequisites

Ensure you have the following libraries installed:

- python3 environment

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/rudrodip/Harmonic-Oscillator-CV
cd Harmonic-Oscillator-CV
```

2. Install the required libraries (see Prerequisites).
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main application script:

```bash
python app.py
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

following is the equation that I'm using for the under-damped oscillation function

$$
x(t) = A e^{-\gamma t} \cos(2\pi f t + \phi) + C
$$

following is the equation that I'm using for decaying oscillation component

$$
x(t) = C \pm A e^{-\gamma t}
$$

following is the equation that I'm using for circle residual

$$
\sqrt{(x - a)^2 + (y - b)^2} - r
$$

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