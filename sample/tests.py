import sys
from PySide import QtCore, QtGui
import pyqtgraph as pg
import random
import csv

sys.path.append('../util')
from PacketParser import PacketParser

parser = PacketParser()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.plot_widget = PlottingWidget(self)
        self.plot_widget.button.clicked.connect(self.plotter)
        self.central_widget.addWidget(self.plot_widget)

        self.csvfile = open( "C:/Users/abad_/Downloads/data.csv", 'rb')
        self.file = csv.reader(self.csvfile, delimiter=',', quotechar='|')
        self.headers = next(self.file)

    def plotter(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)

    def updater(self):
        nextPacket = next(self.file)
        parsed = parser.fromCSVToPacket( list(self.headers), nextPacket )
        self.plot_widget.updater( parsed )

class PlottingWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlottingWidget, self).__init__(parent)

        self.electrodes = (
            ('AF3', (15, 150, 255)), ('AF4', (150, 255, 15)), ('F3', (255, 15, 150)), ('F4', (15, 150, 255)),
            ('F7', (150, 255, 15)), ('F8', (255, 15, 150)),
            ('FC5', (15, 150, 255)), ('FC6', (150, 255, 15)), ('T7', (255, 15, 150)), ('T8', (15, 150, 255)),
            ('P7', (150, 255, 15)), ('P8', (255, 15, 150)),
            ('O1', (15, 150, 255)), ('O2', (150, 255, 15))
        )

        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Start Plotting')
        layout.addWidget(self.button)
        self.plots = pg.GraphicsWindow()
        self.plotter()
        layout.addWidget(self.plots)
        self.startTime = pg.ptime.time()
        self.setLayout(layout)

    def plotter(self):
        self.allwaves = []
        for i in xrange(14):
            if i:
                self.plots.nextRow()
            p = self.plots.addPlot()
            if i == 13:
                p.setLabel('bottom', 'Time', 's')
            else:
                p.showAxis('bottom', False)
            p.setLabel('left', self.electrodes[i][0])
            dataX = [0]
            dataY = [0]
            curve = p.plot()
            self.allwaves.append( [p, dataX, dataY, curve] )

    def updater(self, packet):
        now = pg.ptime.time()

        for i in xrange(len(self.allwaves)):
            plot, dataX, dataY, curve = self.allwaves[i]

            if (len(dataY) >= 300):
                dataY.pop(0)
                dataY[0] = 0
                dataX.pop(0)

            dataY.append( packet.sensors[self.electrodes[i][0]]["value"] )
            dataX.append( now - self.startTime )
            curve.setPen(self.electrodes[i][1])
            plot.setLabel('right', packet.sensors[self.electrodes[i][0]]["value"])
            curve.setData( x = dataX, y = dataY )

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

