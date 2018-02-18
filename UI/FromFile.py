# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtGui import *
import numpy as np
import csv

from PlottingWidget import PlottingWidget

sys.path.append('../util')
from PacketParser import PacketParser

from emokit.util import get_quality_scale_level_color

class FromFile:
    def __init__(self, parent=None):
        self.electrodesPosition = \
            {
                "AF3": {"x": 82, "y": 57},  # AF3
                "AF4": {"x": 221, "y": 57},  # AF4
                "F7": {"x": 35, "y": 104},  # F7
                "F3": {"x": 114, "y": 107},  # F3
                "F4": {"x": 190, "y": 107},  # F4
                "F8": {"x": 269, "y": 104},  # F8
                "FC5": {"x": 67, "y": 149},  # FC5
                "FC6": {"x": 236, "y": 149},  # FC6
                "T7": {"x": 18, "y": 197},  # T7
                "T8": {"x": 286, "y": 197},  # T8
                "P7": {"x": 67, "y": 317},  # P7
                "P8": {"x": 236, "y": 317},  # P8
                "O1": {"x": 113, "y": 375},  # O1
                "O2": {"x": 192, "y": 375}  # O2
            }

        self.headsetColors = \
            [
                (0, 0, 0),      # Black
                (255, 0, 0),    # Red
                (230, 255, 0),  # Yellow
                (102, 175, 54), # Green
            ]
        self.parser = PacketParser()

        self.timer = pg.QtCore.QTimer()

    def setFromFileTab(self):
        self.setLeftSidedBox()
        self.setCenterBox()

        # Bottom sided box
        textEdit2 = QTextEdit("Bottom rectangle")

        # Main grid layout
        self.gridLayout = QGridLayout()
        self.gridLayout.addLayout( self.leftBox, 0, 0)
        self.gridLayout.addLayout( self.centerBox, 0, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        return self.gridLayout

    def setLeftSidedBox(self):
        # Left sided box for controls
        self.leftBox = QFormLayout()

        # Folder selection buttons
        self.route = QLineEdit()
        self.route.setReadOnly(True)
        self.examine = QPushButton("Examinar")
        self.examine.clicked.connect(self.getFilename)

        folderButtons = QGridLayout()
        folderButtons.addWidget(self.route, 0, 0)
        folderButtons.addWidget(self.examine, 0, 1)
        self.leftBox.addRow(QLabel("Archivo escogido"))
        self.leftBox.addRow(folderButtons)

        # Action selection buttons

        self.startBtn = QPushButton("Iniciar")
        self.startBtn.setEnabled(False)
        self.startBtn.clicked.connect(self.startReading)
        self.stopBtn = QPushButton("Pausar")
        self.stopBtn.setEnabled(False)
        self.stopBtn.clicked.connect(self.stopReading)
        self.restartBtn = QPushButton("Reiniciar")
        self.restartBtn.setEnabled(False)
        self.restartBtn.clicked.connect(self.restartReading)

        actionsButtons = QGridLayout()
        actionsButtons.addWidget(self.startBtn, 0, 0)
        actionsButtons.addWidget(self.stopBtn, 0, 1)
        actionsButtons.addWidget(self.restartBtn, 0, 2)
        self.leftBox.addRow(QLabel("Control"))
        self.leftBox.addRow(actionsButtons)

        # Sensors status
        self.leftBox.addRow(QLabel("Estado de los sensores"))
        self.headsetState = QLabel()
        self.leftBox.addRow(self.headsetState)
        self.updateHeadsetStatus( None )

    def setCenterBox(self):
        # Center sided box for signals
        self.centerBox = QFormLayout()
        self.centerBox.addRow(QLabel("Estado de las senales"))

        self.plots = PlottingWidget()
        self.centerBox.addRow( self.plots )

    def updateHeadsetStatus(self, packet):
        pixmap = QPixmap("../assets/headset.png")

        painter = QPainter()
        painter.begin(pixmap)
        if packet == None:
            color = self.headsetColors[0]
            painter.setBrush(QColor(color[0], color[1], color[2]))
            for item in self.electrodesPosition:
                painter.drawEllipse(self.electrodesPosition[item]["x"], self.electrodesPosition[item]["y"], 28, 28)
        else:
            for sensor in packet.sensors:
                if sensor in self.electrodesPosition:
                    quality = packet.sensors[sensor]['quality'] // 540
                    color = self.headsetColors[ quality if quality <= 3 else 3 ]
                    painter.setBrush(QColor(color[0], color[1], color[2]))
                    painter.drawEllipse(self.electrodesPosition[sensor]["x"], self.electrodesPosition[sensor]["y"], 28, 28)

        painter.end()

        self.headsetState.setPixmap(pixmap)

    def startReading(self):
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)

        self.timer.timeout.connect( self.setupNewPacket )
        self.timer.start(10)

    def stopReading(self):
        self.timer.stop()

        self.stopBtn.setEnabled(False)
        self.startBtn.setEnabled(True)

    def restartReading(self):
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        self.restartBtn.setEnabled(False)

        self.timer.stop()

        self.fileRoute = ""
        self.route.setText(self.fileRoute)

        self.csvfile = None
        self.file = None
        self.headers = None

        self.plots.restartPlotting()
        self.updateHeadsetStatus(None)

    def setupNewPacket(self):
        nextPacket = next(self.file)
        parsed = self.parser.fromCSVToPacket( list(self.headers), nextPacket )
        self.plots.updater( parsed )
        self.updateHeadsetStatus(parsed)


    def getFilename(self):
        filename = QFileDialog.getOpenFileName(self.examine, 'Open file',
                                            'c:\\', "CSV (*.csv)")
        self.fileRoute = filename[0]
        self.route.setText( self.fileRoute )

        self.csvfile = open(self.fileRoute, 'rb')
        self.file = csv.reader(self.csvfile, delimiter=',', quotechar='|')
        self.headers = next(self.file)

        self.startBtn.setEnabled(True)
        self.restartBtn.setEnabled(True)