# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide import QtGui, QtCore


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.text = "test"

        self.setGeometry(300, 300, 280, 170)

        self.show()
        self.showMaximized()

    def paintEvent(self, event):
        image = QtGui.QImage("../assets/headset.png")
        painter = QtGui.QPainter(image)
        #painter.begin(self)

        #painter.drawImage(QtCore.QPoint(0, 0), image)
        painter.setBrush(QtGui.QColor(102, 175, 54))
        painter.drawEllipse(82, 57, 28, 28)
        painter.drawEllipse(221, 57, 28, 28)

        painter.drawEllipse(35, 104, 28, 28)
        painter.drawEllipse(114, 107, 28, 28)
        painter.drawEllipse(190, 107, 28, 28)
        painter.drawEllipse(269, 104, 28, 28)

        painter.drawEllipse(67, 149, 28, 28)
        painter.drawEllipse(236, 149, 28, 28)

        painter.drawEllipse(18, 197, 28, 28)
        painter.drawEllipse(286, 197, 28, 28)
        painter.
        #painter.end()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()