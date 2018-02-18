# !/usr/bin/python
# -*- coding: utf-8 -*-

from PySide.QtGui import *

from emokit.emotiv import Emotiv

from PlottingWidget import PlottingWidget
from HeadStatusWidget import HeadStatusWidget

class Record:
    def __init__(self, parent=None):
        self.electrodesPosition = \
            [
                {"x": 82, "y": 57},  # AF3
                {"x": 221, "y": 57},  # AF4
                {"x": 35, "y": 104},  # F7
                {"x": 114, "y": 107},  # F3
                {"x": 190, "y": 107},  # F4
                {"x": 269, "y": 104},  # F8
                {"x": 67, "y": 149},  # FC5
                {"x": 236, "y": 149},  # FC6
                {"x": 18, "y": 197},  # T7
                {"x": 286, "y": 197},  # T8
                {"x": 67, "y": 317},  # P7
                {"x": 236, "y": 317},  # P8
                {"x": 113, "y": 375},  # O1
                {"x": 192, "y": 375}  # O2
            ]
        self.headset = Emotiv()

    def update(self):
        packet = self.headset.dequeue()
        if packet != None:
            self.plots.updater(packet)
        self.headsetState.updateHeadsetStatus(packet)


    def setRecordTab(self):
        self.setLeftSidedBox()
        self.setCenterBox()

        # Bottom sided box
        textEdit2 = QTextEdit("Bottom rectangle")

        # Main grid layout
        self.gridLayout = QGridLayout()
        self.gridLayout.addLayout( self.leftBox, 0, 0)
        self.gridLayout.addLayout( self.centerBox, 0, 1)
        self.gridLayout.addWidget(textEdit2, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 3)

        self.gridLayout.setRowStretch(0, 3)
        self.gridLayout.setRowStretch(1, 1)
        return self.gridLayout

    def setLeftSidedBox(self):
        # Left sided box for controls
        self.leftBox = QFormLayout()

        self.recordButton = QPushButton("Grabar")
        self.stopButton = QPushButton("Detener")
        self.recordButtons = QGridLayout()
        self.recordButtons.addWidget( self.recordButton, 0, 0)
        self.recordButtons.addWidget( self.stopButton, 0, 1)
        self.leftBox.addRow(QLabel("Controles de grabacion"))
        self.leftBox.addRow(self.recordButtons)

        self.route = QLineEdit()
        self.route.setReadOnly(True)
        self.examine = QPushButton("Examinar")
        folderButtons = QGridLayout()
        folderButtons.addWidget(self.route, 0, 0)
        folderButtons.addWidget(self.examine, 0, 1)
        self.leftBox.addRow(QLabel("Carpeta de guardado"))
        self.leftBox.addRow(folderButtons)

        # Sensors status
        self.leftBox.addRow(QLabel("Estado de los sensores"))
        self.headsetState = HeadStatusWidget()
        self.leftBox.addRow(self.headsetState)
        self.headsetState.updateHeadsetStatus(None)

    def setCenterBox(self):
        # Center sided box for signals
        self.centerBox = QFormLayout()
        self.plots = PlottingWidget()
        self.centerBox.addRow(QLabel("Estado de las senales"))
        self.centerBox.addRow(self.plots)