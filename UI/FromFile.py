# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtGui import *
import numpy as np
import csv

sys.path.append('../util')
from PacketParser import PacketParser

from emokit.util import get_quality_scale_level_color

class FromFile:
    def __init__(self, parent=None):
        self.electrodes = (
        ('AF3', (15, 150, 255)), ('AF4', (150, 255, 15)), ('F3', (255, 15, 150)), ('F4', (15, 150, 255)),
        ('F7', (150, 255, 15)), ('F8', (255, 15, 150)),
        ('FC5', (15, 150, 255)), ('FC6', (150, 255, 15)), ('T7', (255, 15, 150)), ('T8', (15, 150, 255)),
        ('P7', (150, 255, 15)), ('P8', (255, 15, 150)),
        ('O1', (15, 150, 255)), ('O2', (150, 255, 15))
        )

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

        # Plot in chunks, adding one new plot curve for every 100 samples
        self.chunkSize = 100
        # Remove chunks after we have 10
        self.maxChunks = 10
        self.startTime = pg.ptime.time()
        #self.headset = Emotiv()

    def update3( self, p, data, ptr, i_curves, startTime, emo_data, color ):
        now = pg.ptime.time()
        for c in i_curves:
            c.setPos(-(now - startTime), 0)

        i = ptr % self.chunkSize
        if i == 0:
            curve = p.plot()
            curve.setPen(color)  # (255, 125, 123))
            i_curves.append(curve)
            last = data[-1]
            data = np.empty((self.chunkSize + 1, 2))
            data[0] = last
            while len(i_curves) > self.maxChunks:
                c = i_curves.pop(0)
                p.removeItem(c)
        else:
            curve = i_curves[-1]
        data[i + 1, 0] = now - startTime
        data[i + 1, 1] = emo_data / 4000  # np.random.normal()  # dummy data  #
        # print emo_data
        # data[i + 1, 1] = ef.process_decrypted_packet_queue(raw_decrypted_packet, processed_packets)
        curve.setData(x=data[:i + 2, 0], y=data[:i + 2, 1])
        ptr += 1
        return [p, data, ptr, i_curves]

    # update all plots
    def update( self, packet ):
        if packet is not None:
            for i, wave in enumerate(self.allWaves):
                wave = self.update3(*wave, startTime=self.startTime, emo_data=packet.sensors[ self.electrodes[i][0]]['value'],
                               color = self.electrodes[i][1])
                self.allWaves[i] = wave

    def setFromFileTab(self):
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
        self.stopBtn = QPushButton("Detener")
        self.stopBtn.setEnabled(False)
        self.stopBtn.clicked.connect(self.stopReading)

        actionsButtons = QGridLayout()
        actionsButtons.addWidget(self.startBtn, 0, 0)
        actionsButtons.addWidget(self.stopBtn, 0, 1)
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
        self.plots = pg.GraphicsWindow()
        self.centerBox.addRow(QLabel("Estado de las senales"))
        self.centerBox.addRow(self.plots)

        self.allWaves = []
        for i in xrange(14):
            if i:
                self.plots.nextRow()
            p = self.plots.addPlot()
            # p.setPen((255, 125, 123))
            if i == 13:
                p.setLabel('bottom', 'Time', 's')
            else:
                p.showAxis('bottom', False)
            # p.setXRange(-10, 0)
            curves = []
            data = np.empty((self.chunkSize + 1, 2))
            ptr = 0
            self.allWaves.append([p, data, ptr, curves])

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
        self.csvfile = open( self.fileRoute, 'rb')
        self.file = csv.reader(self.csvfile, delimiter=',', quotechar='|')
        self.headers = next(self.file)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect( self.setupNewPacket )
        self.timer.start(10)

    def stopReading(self):
        return None

    def setupNewPacket(self):
        nextPacket = next(self.file)
        parsed = self.parser.fromCSVToPacket( list(self.headers), nextPacket )
        self.update( parsed )
        self.updateHeadsetStatus(parsed)


    def getFilename(self):
        filename = QFileDialog.getOpenFileName(self.examine, 'Open file',
                                            'c:\\', "CSV (*.csv)")
        self.fileRoute = filename[0]
        self.route.setText( self.fileRoute )
        self.startBtn.setEnabled(True)