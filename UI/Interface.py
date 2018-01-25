# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtCore import Qt
from PySide.QtGui import *

from Record import Record

from emokit.emotiv import Emotiv
from emokit.util import get_quality_scale_level_color

import numpy as np

class Interface ( QTabWidget ):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

        self.electrodes = (('AF3', (15, 150, 255)), ('AF4', (150, 255, 15)), ('F3', (255, 15, 150)), ('F4', (15, 150, 255)),
                            ('F7', (150, 255, 15)), ('F8', (255, 15, 150)),
                            ('FC5', (15, 150, 255)), ('FC6', (150, 255, 15)), ('T7', (255, 15, 150)), ('T8', (15, 150, 255)),
                            ('P7', (150, 255, 15)), ('P8', (255, 15, 150)),
                            ('O1', (15, 150, 255)), ('O2', (150, 255, 15))
                            )

        self.electrodesPosition = \
        [
            {"x":  82, "y":  57},   #AF3
            {"x": 221, "y":  57},   #AF4
            {"x":  35, "y": 104},   #F7
            {"x": 114, "y": 107},   #F3
            {"x": 190, "y": 107},   #F4
            {"x": 269, "y": 104},   #F8
            {"x":  67, "y": 149},   #FC5
            {"x": 236, "y": 149},   #FC6
            {"x":  18, "y": 197},   #T7
            {"x": 286, "y": 197},   #T8
            {"x":  67, "y": 317},   #P7
            {"x": 236, "y": 317},   #P8
            {"x": 113, "y": 375},   #O1
            {"x": 192, "y": 375}    #O2
        ]

        # Plot in chunks, adding one new plot curve for every 100 samples
        self.chunkSize = 100
        # Remove chunks after we have 10
        self.maxChunks = 10
        self.startTime = pg.ptime.time()

        self.recordTab = Record()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.tab1UI()
        self.tab2UI()
        self.setWindowTitle("Emokit Visualizer")
        self.showMaximized()

    def tab1UI(self):
        self.setTabText(0, "Grabar")
        self.tab1.setLayout( self.recordTab.setRecordTab() )

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.recordTab.update)
        self.timer.start(10)

    def tab2UI(self):
        # Left sided box for controls
        leftBox = QFormLayout()

        route = QLineEdit()
        route.setReadOnly(True)
        examine = QPushButton("Examinar")
        folderButtons = QGridLayout()
        folderButtons.addWidget(route, 0, 0)
        folderButtons.addWidget(examine, 0, 1)
        leftBox.addRow(QLabel("Ruta del archivo"))
        leftBox.addRow(folderButtons)

        self.setTabText(1, "Desde archivo")
        self.tab2.setLayout(leftBox)

def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()