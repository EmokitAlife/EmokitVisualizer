from distutils.core import setup

setup(
    name = 'emokit', # temporal
    version = "0.1",
    description = "An Open Source signal visualizer for the Emotiv EPOC+ Dongle",
    author = "Universidad Nacional de Colombia",
    author_email = "datovard@unal.edu.co",
    py_modules=['sample', 'user-interface']
    #packages=find_packages(exclude=('tests', 'docs'))
)