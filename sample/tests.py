import sys
from PySide import QtCore, QtGui
import pyqtgraph as pg
import random
import csv

sys.path.append('../util')
sys.path.append('../UI')
from PacketParser import PacketParser
from PlottingWidget import PlottingWidget

parser = PacketParser()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.plot_widget = PlottingWidget(self)
        self.central_widget.addWidget(self.plot_widget)

        self.plotter()
        self.plot_widget.button.clicked.connect(self.stopPlotting)

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

    def stopPlotting(self):
        self.timer.stop()
        self.plot_widget.restartPlotting()
        self.plotter()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

