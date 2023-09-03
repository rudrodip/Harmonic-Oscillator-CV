import numpy as np

# initial guess
initial_guess = [300, 0.04, 2.919, -1.8, 200]

# bounds
lower_bounds = [0, -np.inf, 0, -np.inf, -np.inf]  # A, gamma, w, phi, C
upper_bounds = [np.inf, np.inf, np.inf, np.inf, np.inf]

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)
ORANGE = (0, 165, 255)
PINK = (147, 20, 255)
PURPLE = (128, 0, 128)
BROWN = (42, 42, 165)