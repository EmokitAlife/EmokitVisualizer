import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import scipy.fftpack
import scipy.signal as signal

fig, ax = plt.subplots(3)
plt.subplots_adjust(bottom=0.2)

class Index(object):
    ind = 0
    data = {}
    PACKET_SIZE = 127

    def __init__(self):
        nombre = raw_input("Nombre del archivo: ")
        self.sensor = raw_input("Nombre del sensor: ").strip()
        with open(nombre) as openfileobject:
            for line in openfileobject:
                line = line.strip().split(" ")
                if (line[0] not in self.data): self.data[line[0]] = []
                self.data[line[0]].append( int(line[1]) )

            y = self.data[self.sensor]
            x = np.arange(0.0, len(y), 1 )

            windowx = np.arange(0.0, self.PACKET_SIZE, 1)
            window = np.hamming( self.PACKET_SIZE )
            windowed = self.detrend(y[0:self.PACKET_SIZE]) * window
            windowedyf = scipy.fftpack.fft(windowed)
            windowedxf = np.linspace(0.0, 40.0, num=40.0)

            yf = scipy.fftpack.fft(y)
            xf = np.linspace(0.0, 40.0, num=40.0)

            self.l1 = ax[0].plot(x, y, windowx, window*np.amax(y), windowx, window*(-1*np.amax(y)))
            self.l2 = ax[1].plot(windowx, self.detrend(y[0:self.PACKET_SIZE]), windowx, windowed, lw=2)
            self.l3, = ax[2].plot(windowedxf, np.abs(windowedyf[:40]), lw=2)
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
        i = self.ind % (len(self.data[self.sensor])//self.PACKET_SIZE)

        y = self.detrend( (self.data[self.sensor])[i * self.PACKET_SIZE:(i + 1) * self.PACKET_SIZE] )

        windowx = np.arange(i*self.PACKET_SIZE, (i+1)*self.PACKET_SIZE, 1)
        window = np.hamming(self.PACKET_SIZE)
        windowed = y * window
        windowedyf = scipy.fftpack.fft(windowed)

        self.l1[1].set_xdata(windowx)
        self.l1[2].set_xdata(windowx)
        self.l2[0].set_ydata( y )
        self.l2[1].set_ydata( windowed )
        self.l3.set_ydata(np.abs(windowedyf[:40]))

        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % (len(self.data[self.sensor])// self.PACKET_SIZE)

        y = self.detrend( (self.data[self.sensor])[i * self.PACKET_SIZE:(i + 1) * self.PACKET_SIZE] )

        windowx = np.arange(i * self.PACKET_SIZE, (i + 1) * self.PACKET_SIZE, 1)
        window = np.hamming(self.PACKET_SIZE)
        windowed = y * window
        windowedyf = scipy.fftpack.fft(windowed)

        self.l1[1].set_xdata(windowx)
        self.l1[2].set_xdata(windowx)
        self.l2[0].set_ydata(y)
        self.l2[1].set_ydata(windowed)
        self.l3.set_ydata(np.abs(windowedyf[:40]))

        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()