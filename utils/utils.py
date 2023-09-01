import json
import numpy as np

def load_json(filename):
  try:
    with open(filename, "r") as f:
      hsv = json.load(f)
      return hsv
  except:
    print(f'cant load {filename}. returning default hsv value')
    return { }

def save_json(filename, jsonfile):
    with open(filename, "w") as f:
        json.dump(jsonfile, f)

    print(f'Saved {filename}')

def underdamped_harmonic_oscillator(t, A, gamma, f, phi, C):
    return A * np.exp(-gamma * t) * np.cos(2 * np.pi * f * t + phi) + C

def upper_decaying_component_curve(t, A, gamma, C):
    return C + A * np.exp(-gamma * t)

def lower_decaying_component_curve(t, A, gamma, C):
    return C - A * np.exp(-gamma * t)