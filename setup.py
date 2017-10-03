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
    install_requires = [
        "pycrypto>=2.6.1",
        "future",
        "pytest",
        "emokit",
        "pygame"
        ] + ["pywinusb>=0.4.2"] if "win" in sys.platform else []
        + [],
    license = "MIT License",
    url = "https://github.com/EmokitAlife/EmokitVisualizer"
    #packages=find_packages(exclude=('tests', 'docs'))
)