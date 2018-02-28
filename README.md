# EmokitVisualizer

This is an Open Source signal visualizer project for the Emotiv EPOC+ Dongle based on the open source project [Emokit](https://github.com/openyou/emokit)

## Screenshots

![alt text](https://github.com/EmokitAlife/EmokitVisualizer/blob/CreacionUI/assets/screenshot-1.png "Main Interface")
![alt text](https://github.com/EmokitAlife/EmokitVisualizer/blob/CreacionUI/assets/screenshot-2.png "Main Interface")


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

First, if you are in a Windows machine, you should install the Microsoft Visual C++ Compiler for Python
It depends on the version of Python of your preference, for example, here is the [link](https://www.microsoft.com/en-us/download/details.aspx?id=44266) for Python 2.7


### Installing

#### Windows

After you have installed the Visual C++ Compiler, you have to start a cmd console in the folder that holds your project and type:

```
pip install -r requirements.txt
```

This command will install all the Python modules needed for running the Emokit driver package

### Linux ( Debian based )

First, you have to install the Hidapi driver so your OS can read the USB-HID that comes with the dongle, so you have to install this libraries, open your terminal and run:

```
sudo apt-get install libudev-dev libusb-1.0-0-dev libtool dh-autoreconf
```

After that, you got to download and install the 'Hidapi' driver itself, download the last version here:

```
https://github.com/signal11/hidapi/archive/master.zip
```

Now that you have the driver, you have to get a C++ compiler like 'g++' to compile and install the driver, after that, we have to unzip, compile and install the driver, open a Terminal at your Downloads folder:

```
unzip hidapi-master.zip
cd hidapi-master
./bootstrap
./configure
make
sudo make install
```

Now we have to install a Python library that connects the 'Hidapi' driver with your Python project, that can be made with the library 'pyhidapi', go to this link and download it:

```
https://pypi.python.org/pypi/hid/0.1.1
```

Or, you can download it from it's Main Github project in:

```
https://github.com/NF6X/pyhidapi
```

In this example, we download it from it's Github project, open a Terminal in your Downloads folder again and type:

```
unzip pyhidapi-master.zip
cd pyhidapi-master
python setup.py install
```

After installing the 'pyhidapi', we can run the main requirements setup, download it, we have to make a little fix in the 'requirements.txt' file first, open it in your favorite text editor and remove the line that says:

```
pywinusb>=0.4.2
```

This is the USB-HID driver for Windows, we are removing it because, in the Linux case, we are using the 'Hidapi' driver instead

After that, open a Terminal in the folder of the project and run:

```
pip install -r requirements.txt
```

And that's it for Linux.

## Authors

* **Dorian Tovar** - *developer* - [datovard](https://github.com/datovard)

See also the list of [contributors](https://github.com/orgs/EmokitAlife/people) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
