try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys
import re

setup(
    name = 'emokitvisualizer', # temporal
    version = "0.1",
    description = "An Open Source signal visualizer for the Emotiv EPOC+ Dongle",
    author = "Universidad Nacional de Colombia",
    author_email = "datovard@unal.edu.co",
    py_modules=['sample', 'user-interface'],
    license = "MIT License",
    url = "https://github.com/EmokitAlife/EmokitVisualizer"
)