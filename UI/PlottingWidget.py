from PySide import QtCore, QtGui
import pyqtgraph as pg

class PlottingWidget(QtGui.QWidget):
    def __init__(self, sensors=None, parent=None):
        super(PlottingWidget, self).__init__(parent)

        self.electrodes = (
            ('AF3', (15, 150, 255)), ('AF4', (150, 255, 15)), ('F3', (255, 15, 150)), ('F4', (15, 150, 255)),
            ('F7', (150, 255, 15)), ('F8', (255, 15, 150)),
            ('FC5', (15, 150, 255)), ('FC6', (150, 255, 15)), ('T7', (255, 15, 150)), ('T8', (15, 150, 255)),
            ('P7', (150, 255, 15)), ('P8', (255, 15, 150)),
            ('O1', (15, 150, 255)), ('O2', (150, 255, 15))
        )

        layout = QtGui.QHBoxLayout()
        pg.setConfigOptions(antialias=True)
        self.plots = pg.GraphicsWindow()
        layout.addWidget(self.plots)
        self.setLayout(layout)
        self.sensors = sensors
        self.startTime = pg.ptime.time()
        self.plotter()

    def restartSensors(self, sensors):
        self.sensors = sensors
        self.startTime = pg.ptime.time()
        self.restartPlotting()

    def plotter(self):
        self.allwaves = []
        if self.sensors == None:
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
        else:
            for i, sensor in enumerate(self.sensors):
                if i:
                    self.plots.nextRow()
                p = self.plots.addPlot()
                if i == len(self.sensors)-1:
                    p.setLabel('bottom', 'Time', 's')
                else:
                    p.showAxis('bottom', False)
                p.setLabel('left', sensor)
                dataX = [0]
                dataY = [0]
                curve = p.plot()
                self.allwaves.append([p, dataX, dataY, curve])

    def updater(self, packet):
        now = pg.ptime.time()
        if self.sensors == None:
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
        else:
            for i, sensor in enumerate(self.sensors):
                plot, dataX, dataY, curve = self.allwaves[i]

                if (len(dataY) >= 300):
                    dataY.pop(0)
                    dataY[0] = 0
                    dataX.pop(0)

                dataY.append(packet.sensors[sensor]["value"])
                dataX.append(now - self.startTime)
                curve.setPen(self.electrodes[i][1])
                plot.setLabel('right', packet.sensors[sensor]["value"])
                curve.setData(x=dataX, y=dataY)


    def restartPlotting(self):
        self.plots.clear()
        self.plots.nextRow()
        self.plotter()