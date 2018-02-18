# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtGui import *
import csv

from PlottingWidget import PlottingWidget
from HeadStatusWidget import HeadStatusWidget

sys.path.append('../util')
from PacketParser import PacketParser

class FromFile:
    def __init__(self, parent=None):
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

        self.headsetState = HeadStatusWidget()
        self.leftBox.addRow(self.headsetState)
        self.headsetState.updateHeadsetStatus(None)

    def setCenterBox(self):
        # Center sided box for signals
        self.centerBox = QFormLayout()
        self.centerBox.addRow(QLabel("Estado de las senales"))

        self.plots = PlottingWidget()
        self.centerBox.addRow( self.plots )

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
        self.headsetState.updateHeadsetStatus(None)

    def setupNewPacket(self):
        nextPacket = next(self.file)
        parsed = self.parser.fromCSVToPacket( list(self.headers), nextPacket )
        self.plots.updater( parsed )
        self.headsetState.updateHeadsetStatus(parsed)

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