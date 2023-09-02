from setuptools import setup, find_packages

# Project metadata
name = "Harmonic Oscillator CV"
version = "0.0.2"  # Replace with your project version
description = "This Python project is designed to analyze the harmonic oscillation of an object using computer vision techniques."
author = "Rudrodip Sarker"
author_email = "official.rudrodipsarker@gmail.com"
url = "https://github.com/rudrodip/Harmonic-Oscillator-CV"
license = "MIT"

# Project dependencies
with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Packages to include
packages = find_packages()

# Long description (optional)
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=packages,
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
