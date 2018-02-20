from PySide.QtGui import *
from PySide.QtCore import Qt

class HeatMapWidget(QWidget):
    def __init__(self, parent=None):
        super(HeatMapWidget, self).__init__(parent)

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
                (0, 0, 255),  # Black
                (21, 0, 234),  # Red
                (43, 0, 212),  # Yellow
                (64, 0, 191),  # Green
                (106, 0, 149),
                (128, 0, 128),
                (149, 0, 106),
                (170, 0, 85),
                (191, 0, 64),
                (212, 0, 43),
                (234, 0, 21),
                (255, 0, 0)
            ]

        layout = QHBoxLayout()
        self.headsetState = QLabel()
        layout.addWidget(self.headsetState)
        self.setLayout(layout)
        self.minValue = -607
        self.maxValue = 3075

    def updateHeatMapStatus(self, packet):
        pixmap = QPixmap("../assets/headset.png")

        painter = QPainter()
        painter.begin(pixmap)

        painter.setFont(QFont('Decorative', 15))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "Mapa de calor")

        painter.setFont(QFont('Decorative', 8))

        for key in self.electrodesPosition:
            if key[0] == "O":
                painter.drawText(self.electrodesPosition[key]["x"] - 1, self.electrodesPosition[key]["y"] - 20, 30, 15,
                                 Qt.AlignCenter, key)
            elif key == "T7":
                painter.drawText(self.electrodesPosition[key]["x"] + 7, self.electrodesPosition[key]["y"] + 32, 30, 15,
                                 Qt.AlignCenter, key)
            elif key == "T8":
                painter.drawText(self.electrodesPosition[key]["x"] - 9, self.electrodesPosition[key]["y"] + 32, 30, 15,
                                 Qt.AlignCenter, key)
            else:
                painter.drawText( self.electrodesPosition[key]["x"] - 1, self.electrodesPosition[key]["y"] + 32, 30, 15, Qt.AlignCenter, key)

        if packet == None:
            color = self.headsetColors[0]
            painter.setBrush(QColor(0,0,0))
            for item in self.electrodesPosition:
                painter.drawEllipse(self.electrodesPosition[item]["x"], self.electrodesPosition[item]["y"], 28, 28)
        else:
            for sensor in packet.sensors:
                if sensor in self.electrodesPosition:
                    quality = ( packet.sensors[sensor]['value'] + -1*self.minValue ) // 307
                    color = self.headsetColors[ quality ]
                    painter.setBrush(QColor(color[0], color[1], color[2]))
                    painter.drawEllipse( self.electrodesPosition[sensor]["x"], self.electrodesPosition[sensor]["y"], 28, 28)
        painter.end()

        self.headsetState.setPixmap(pixmap)
