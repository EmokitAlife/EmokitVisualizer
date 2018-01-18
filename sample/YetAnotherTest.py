# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PySide.QtCore import Qt
from PySide.QtGui import *

class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.label = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 3, Qt.AlignCenter)
        self.setLayout(layout)

        self.updateHeadsetStatus()

    def updateHeadsetStatus(self):
        pixmap = QPixmap("../assets/headset.png")

        painter = QPainter()
        painter.begin(pixmap)
        painter.setBrush(QColor(102, 175, 54))

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

        painter.drawEllipse(67, 317, 28, 28)
        painter.drawEllipse(236, 317, 28, 28)

        painter.drawEllipse(113, 375, 28, 28)
        painter.drawEllipse(192, 375, 28, 28)

        painter.end()

        self.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
