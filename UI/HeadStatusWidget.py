from PySide.QtGui import *
import pyqtgraph as pg

class HeadStatusWidget(QWidget):
    def __init__(self, parent=None):
        super(HeadStatusWidget, self).__init__(parent)

        self.electrodesPosition = \
            {
                "AF3": {"x": 82, "y": 57},
                "AF4": {"x": 221, "y": 57},
                "F7" : {"x": 35, "y": 104},
                "F3" : {"x": 114, "y": 107},
                "F4" : {"x": 190, "y": 107},
                "F8" : {"x": 269, "y": 104},
                "FC5": {"x": 67, "y": 149},
                "FC6": {"x": 236, "y": 149},
                "T7" : {"x": 18, "y": 197},
                "T8" : {"x": 286, "y": 197},
                "P7" : {"x": 67, "y": 317},
                "P8" : {"x": 236, "y": 317},
                "O1" : {"x": 113, "y": 375},
                "O2" : {"x": 192, "y": 375}
            }

        self.headsetColors = \
            [
                (0, 0, 0),  # Black
                (255, 0, 0),  # Red
                (230, 255, 0),  # Yellow
                (102, 175, 54),  # Green
            ]

        layout = QHBoxLayout()
        self.headsetState = QLabel()
        layout.addWidget(self.headsetState)
        self.setLayout(layout)

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
                    painter.drawEllipse( self.electrodesPosition[sensor]["x"], self.electrodesPosition[sensor]["y"], 28, 28)
        painter.end()

        self.headsetState.setPixmap(pixmap)