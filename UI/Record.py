# !/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtGui import *
from emokit.emotiv import Emotiv
from PlottingWidget import PlottingWidget
from HeadStatusWidget import HeadStatusWidget

class Record:
    def __init__(self, parent=None):
        self.headset = Emotiv()
        self.electrodePairing = { \
            "AF3": {'pair': "AF4", 'order': 1},
            "AF4": {'pair': "AF3", 'order': 0},
            "F3": {'pair': "F4", 'order': 1},
            "F4": {'pair': "F3", 'order': 0},
            "F7": {'pair': "F8", 'order': 1},
            "F8": {'pair': "F7", 'order': 0},
            "FC5": {'pair': "FC6", 'order': 1},
            "FC6": {'pair': "FC5", 'order': 0},
            "T7": {'pair': "T8", 'order': 1},
            "T8": {'pair': "T7", 'order': 0},
            "P7": {'pair': "P8", 'order': 1},
            "P8": {'pair': "P7", 'order': 0},
            "O1": {'pair': "O2", 'order': 1},
            "O2": {'pair': "O1", 'order': 0},
        }

    def setPlotGraphBySensor(self, sensor):
        self.plots.setVisible(False)
        self.altPlots.setVisible(True)

        if self.electrodePairing[sensor]["order"]:
            self.altPlots.restartSensors( [ sensor, self.electrodePairing[sensor]["pair"]] )
        else:
            self.altPlots.restartSensors([ self.electrodePairing[sensor]["pair"], sensor ])

        self.returnToGraphs.setVisible(True)

    def update(self):
        packet = self.headset.dequeue()
        if packet != None:
            self.plots.updater(packet)
        self.headsetState.updateHeadsetStatus(packet)


    def setRecordTab(self):
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

        self.recordButton = QPushButton("Grabar")
        self.recordButton.setEnabled(False)

        self.stopButton = QPushButton("Detener")
        self.stopButton.setEnabled(False)
        self.recordButtons = QGridLayout()
        self.recordButtons.addWidget( self.recordButton, 0, 0)
        self.recordButtons.addWidget( self.stopButton, 0, 1)
        self.leftBox.addRow(QLabel("Controles de grabacion"))
        self.leftBox.addRow(self.recordButtons)

        self.route = QLineEdit()
        self.route.setReadOnly(True)
        self.examine = QPushButton("Examinar")
        self.examine.clicked.connect(self.getFilename)
        folderButtons = QGridLayout()
        folderButtons.addWidget(self.route, 0, 0)
        folderButtons.addWidget(self.examine, 0, 1)
        self.leftBox.addRow(QLabel("Carpeta de guardado"))
        self.leftBox.addRow(folderButtons)

        # Sensors status
        self.leftBox.addRow(QLabel("Estado de los sensores"))
        self.headsetState = HeadStatusWidget(self.setPlotGraphBySensor)
        self.leftBox.addRow(self.headsetState)
        self.headsetState.updateHeadsetStatus(None)

    def setCenterBox(self):
        # Center sided box for signals
        self.centerBox = QFormLayout()

        self.centerBox.addRow(QLabel("Estado de las senales"))

        self.returnToGraphs = QPushButton("Regresar")
        self.returnToGraphs.setVisible(False)
        self.returnToGraphs.clicked.connect(self.returnToGraphics)
        self.centerBox.addRow(self.returnToGraphs)

        self.plots = PlottingWidget()
        self.centerBox.addRow(self.plots)

        self.altPlots = PlottingWidget([])
        self.centerBox.addRow(self.altPlots)
        self.altPlots.setVisible(False)

    def returnToGraphics(self):
        self.altPlots.setVisible(False)
        self.returnToGraphs.setVisible(False)
        self.plots.setVisible(True)

    def getFilename(self):
        filename = QFileDialog.getExistingDirectory(self.examine, "Open Directory",
                                         "/home",
                                         QFileDialog.ShowDirsOnly
                                         | QFileDialog.DontResolveSymlinks);
        self.fileRoute = filename
        self.route.setText(self.fileRoute)

        self.recordButton.setEnabled(True)
        self.stopButton.setEnabled(True)