import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import scipy.fftpack
import scipy.signal as signal

freqs = np.arange(2, 20, 3)

fig, ax = plt.subplots(2)
plt.subplots_adjust(bottom=0.2)

class Index(object):
    ind = 0
    data = {}

    def __init__(self):
        nombre = raw_input("Nombre del archivo: ")
        with open(nombre) as openfileobject:
            for line in openfileobject:
                line = line.strip().split(" ")
                if (line[0] not in self.data): self.data[line[0]] = []
                self.data[line[0]].append( int(line[1]) )
            for key in self.data.keys():
                self.data[key] = self.detrend( self.data[key] )

            y = self.data[self.data.keys()[0]]
            x = np.arange(0.0, len(y), 1 )

            yf = scipy.fftpack.fft(y)
            xf = np.linspace(0.0, 40.0, num=40.0)

            self.l1, = ax[0].plot(x, y, lw=2)
            self.l2, = ax[1].plot(xf, np.abs(yf[:40]), lw=2)
            ax[0].set_title(self.data.keys()[0])

    def detrend(self, data):
        y = data
        x = np.arange(0.0, len(y), 1)
        polgrad = 6;
        p = np.polyfit(x, y, polgrad)
        f_y = np.polyval(p, x)
        yadjusted = y - f_y

        return yadjusted

    def next(self, event):
        self.ind += 1
        i = self.ind % len(self.data)
        keys = self.data.keys()
        ydata = self.data[ keys[i] ]
        yf = scipy.fftpack.fft(ydata)
        self.l1.set_ydata(ydata)
        self.l2.set_ydata(np.abs(yf[:40]))
        ax[0].set_title(keys[i])
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(self.data)
        keys = self.data.keys()
        ydata = self.data[keys[i]]
        yf = scipy.fftpack.fft(ydata)
        self.l1.set_ydata(ydata)
        self.l2.set_ydata(np.abs(yf[:40]))
        ax[0].set_title(keys[i])
        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()