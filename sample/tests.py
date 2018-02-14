from PySide import QtCore, QtGui
import pyqtgraph as pg
import random
import csv

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.central_widget.addWidget(self.login_widget)

        self.csvfile = open( "C:/Users/abad_/Downloads/data.csv", 'rb')
        self.file = csv.reader(self.csvfile, delimiter=',', quotechar='|')
        self.headers = next(self.file)

    def plotter(self):
        self.data1 =[0]
        self.data2 = [0]
        self.curve1 = self.login_widget.p1.plot()
        self.curve2 = self.login_widget.p2.plot()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)

    def updater(self):
        nextPacket = next(self.file)
        if( len(self.data1) >= 300 ):
            self.data1.pop(0)
            self.data1[0] = 0
        self.data1.append( int(nextPacket[1]) )

        self.curve1.setData(self.data1)

        if (len(self.data2) >= 300):
            self.data2.pop(0)
            self.data2[0] = 0
        self.data2.append(int(nextPacket[3]))

        self.curve2.setData(self.data2)


class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Start Plotting')
        layout.addWidget(self.button)
        #self.plot = pg.PlotWidget()
        self.plots = pg.GraphicsWindow()

        self.p1 = self.plots.addPlot()
        self.plots.nextRow()
        self.p2 = self.plots.addPlot()

        layout.addWidget(self.plots)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

