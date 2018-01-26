# !/usr/bin/python
# -*- coding: utf-8 -*-

import pyqtgraph as pg
from PySide.QtGui import *
import numpy as np

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
    def update( self ):
        packet = self.headset.dequeue()
        # print packet
        # packet = 1
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

        self.route = QLineEdit()
        self.route.setReadOnly(True)

        self.examine = QPushButton("Examinar")
        self.examine.clicked.connect(self.getFilename)

        folderButtons = QGridLayout()
        folderButtons.addWidget(self.route, 0, 0)
        folderButtons.addWidget(self.examine, 0, 1)
        self.leftBox.addRow(QLabel("Archivo escogido"))
        self.leftBox.addRow(folderButtons)

        # Sensors status
        self.leftBox.addRow(QLabel("Estado de los sensores"))
        self.headsetState = QLabel()
        self.leftBox.addRow(self.headsetState)
        self.updateHeadsetStatus()

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

    def updateHeadsetStatus(self):
        pixmap = QPixmap("../assets/headset.png")

        painter = QPainter()
        painter.begin(pixmap)
        painter.setBrush(QColor(102, 175, 54))

        for item in self.electrodesPosition:
            painter.drawEllipse( item["x"], item["y"], 28, 28)

        painter.end()

        self.headsetState.setPixmap(pixmap)

    def getFilename(self):
        filename = QFileDialog.getOpenFileName(self.examine, 'Open file',
                                            'c:\\', "CSV (*.csv)")
        print filename