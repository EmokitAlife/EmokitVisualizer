# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtGui import *
import csv

from PlottingWidget import PlottingWidget
from HeadStatusWidget import HeadStatusWidget
from HeatMapWidget import HeatMapWidget

sys.path.append('../util')
from PacketParser import PacketParser

class FromFile:
    def __init__(self, parent=None):
        self.parser = PacketParser()
        self.timer = pg.QtCore.QTimer()

        self.electrodePairing = {\
            "AF3": {'pair': "AF4", 'order': 1},
            "AF4": {'pair': "AF3", 'order': 0},
            "F3":  {'pair': "F4", 'order': 1},
            "F4":  {'pair': "F3", 'order': 0},
            "F7":  {'pair': "F8", 'order': 1},
            "F8":  {'pair': "F7", 'order': 0},
            "FC5": {'pair': "FC6", 'order': 1},
            "FC6": {'pair': "FC5", 'order': 0},
            "T7":  {'pair': "T8", 'order': 1},
            "T8":  {'pair': "T7", 'order': 0},
            "P7":  {'pair': "P8", 'order': 1},
            "P8":  {'pair': "P7", 'order': 0},
            "O1":  {'pair': "O2", 'order': 1},
            "O2":  {'pair': "O1", 'order': 0},
        }

    def setFromFileTab(self):
        self.setLeftSidedBox()
        self.setCenterBox()

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

        self.headsetState = HeadStatusWidget(self.setPlotGraphBySensor)
        self.leftBox.addRow(self.headsetState)
        self.headsetState.updateHeadsetStatus(None)

    def setPlotGraphBySensor(self, sensor):
        self.plots.setVisible(False)
        self.heatmap.setVisible(False)
        self.altPlots.setVisible(True)

        if self.electrodePairing[sensor]["order"]:
            self.altPlots.restartSensors( [ sensor, self.electrodePairing[sensor]["pair"]] )
        else:
            self.altPlots.restartSensors([ self.electrodePairing[sensor]["pair"], sensor ])

        self.toggleGraph.setVisible(False)
        self.returnToGraphs.setVisible(True)

    def setCenterBox(self):
        # Center sided box for signals
        self.centerBox = QFormLayout()
        self.centerBox.addRow(QLabel("Estado de las senales"))

        self.activeGraph = True

        self.toggleGraph = QPushButton("Mapa de calor")
        self.toggleGraph.setEnabled( False )
        self.toggleGraph.clicked.connect( self.toggleGraphics )
        self.centerBox.addRow( self.toggleGraph )

        self.returnToGraphs = QPushButton("Regresar")
        self.returnToGraphs.setVisible(False)
        self.returnToGraphs.clicked.connect(self.returnToGraphics)
        self.centerBox.addRow(self.returnToGraphs)

        self.plots = PlottingWidget()
        self.centerBox.addRow( self.plots )

        self.heatmap = HeatMapWidget()
        self.centerBox.addRow(self.heatmap)
        self.toggleGraphics()

        self.altPlots = PlottingWidget([])
        self.centerBox.addRow(self.altPlots)
        self.altPlots.setVisible(False)

    def toggleGraphics(self):
        if not self.activeGraph:
            self.plots.setVisible(False)
            self.heatmap.setVisible(True)
            self.toggleGraph.setText("Graficas")
            self.activeGraph = True
        else:
            self.plots.setVisible(True)
            self.heatmap.setVisible(False)
            self.toggleGraph.setText("Mapa de calor")
            self.activeGraph = False

    def returnToGraphics(self):
        self.altPlots.setVisible(False)
        self.returnToGraphs.setVisible(False)
        self.plots.setVisible(True)
        self.toggleGraph.setVisible(True)

    def startReading(self):
        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(True)
        self.toggleGraph.setEnabled(True)

        self.timer.timeout.connect( self.setupNewPacket )
        self.timer.start(10)

    def stopReading(self):
        self.timer.stop()

        self.stopBtn.setEnabled(False)
        self.startBtn.setEnabled(True)

    def restartReading(self):
        self.altPlots.setVisible(False)
        self.returnToGraphs.setVisible(False)

        self.startBtn.setEnabled(False)
        self.stopBtn.setEnabled(False)
        self.restartBtn.setEnabled(False)
        self.toggleGraph.setEnabled(False)

        self.timer.stop()

        self.fileRoute = ""
        self.route.setText(self.fileRoute)

        self.csvfile = None
        self.file = None
        self.headers = None

        self.plots.restartPlotting()
        self.plots.setVisible(True)
        self.activeGraph = True
        self.heatmap.updateHeatMapStatus(None)
        if self.activeGraph:
            self.toggleGraphics()
        self.headsetState.updateHeadsetStatus(None)

    def setupNewPacket(self):
        nextPacket = next(self.file)
        parsed = self.parser.fromCSVToPacket( list(self.headers), nextPacket )
        self.plots.updater( parsed )
        self.heatmap.updateHeatMapStatus(parsed)
        self.headsetState.updateHeadsetStatus(parsed)
        if self.altPlots != None:
            self.altPlots.updater(parsed)

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