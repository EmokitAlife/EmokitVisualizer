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
        file_num = int(raw_input("Ingrese la cantidad de archivos: ") )
        names = []
        for i in xrange(file_num):
            name =  raw_input( "Nombre del archivo "+str(i+1)+": " ).strip()
            self.data[name] = {}
            with open(name) as openfileobject:
                for line in openfileobject:
                    line = line.strip().split(" ")
                    if (line[0] not in self.data[name]): self.data[name][line[0]] = []
                    self.data[name][line[0]].append( int(line[1]) )

        self.sensor = raw_input("Nombre del sensor: ").strip()
        self.l1 = []
        self.l2 = []
        self.l3 = []

        windowx = np.arange(0.0, self.PACKET_SIZE, 1)
        window = np.hamming(self.PACKET_SIZE)
        cont = 1
        for key in self.data.keys():
            y = self.data[key][self.sensor]
            x = np.arange(0.0, len(y), 1 )

            windowed = self.detrend(y[0:self.PACKET_SIZE]) * window
            windowedyf = scipy.fftpack.fft(windowed)
            windowedxf = np.linspace(0.0, 40.0, num=40.0)

            self.l1.append( ax[0].plot(x, y, label="grafica "+str(cont) ) )
            self.l2.append( ax[1].plot( windowx, windowed ) )
            self.l3.append(ax[2].plot( windowedxf, np.abs(windowedyf[:40]) ))
            cont += 1
        ax[0].set_title(self.sensor)
        self.l1.append(ax[0].plot(windowx, window, label="grafica " + str(cont)))

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
        plotI = 0
        window = np.hamming(self.PACKET_SIZE)

        for key in self.data.keys():
            i = self.ind % (len(self.data[key][self.sensor]) // self.PACKET_SIZE)

            y = self.data[key][self.sensor]
            y_cut = self.detrend( y[i * self.PACKET_SIZE:(i + 1) * self.PACKET_SIZE] )

            windowed = y_cut * window
            windowedyf = scipy.fftpack.fft(windowed)
            windowx = np.arange(i * self.PACKET_SIZE, (i + 1) * self.PACKET_SIZE, 1)

            self.l1[plotI][0].set_ydata(y)
            self.l2[plotI][0].set_ydata(windowed)
            self.l3[plotI][0].set_ydata(np.abs(windowedyf[:40]))
            self.l1[len(self.l1)-1][0].set_xdata(windowx)
            plotI += 1
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        plotI = 0
        window = np.hamming(self.PACKET_SIZE)
        for key in self.data.keys():
            i = self.ind % (len(self.data[key][self.sensor]) // self.PACKET_SIZE)

            y = self.data[key][self.sensor]
            y_cut = self.detrend(y[i * self.PACKET_SIZE:(i + 1) * self.PACKET_SIZE])

            windowed = y_cut * window
            windowedyf = scipy.fftpack.fft(windowed)
            windowx = np.arange(i * self.PACKET_SIZE, (i + 1) * self.PACKET_SIZE, 1)

            self.l1[plotI][0].set_ydata(y)
            self.l2[plotI][0].set_ydata(windowed)
            self.l3[plotI][0].set_ydata(np.abs(windowedyf[:40]))
            self.l1[len(self.l1) - 1][0].set_xdata(windowx)
            plotI += 1

        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()