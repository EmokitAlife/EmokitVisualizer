# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PySide.QtCore import Qt
from PySide.QtGui import *


class Window(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.label = QLabel()

        self.lineEdit = QLineEdit("ABCDE")
        self.fontComboBox = QFontComboBox()
        self.sizeSpinBox = QDoubleSpinBox()
        self.sizeSpinBox.setMinimum(1.0)
        self.sizeSpinBox.setValue(12.0)
        saveButton = QPushButton(self.tr("Save"))

        self.lineEdit.textChanged.connect(self.updateImage)
        self.fontComboBox.currentFontChanged.connect(self.updateImage)
        self.sizeSpinBox.valueChanged.connect(self.updateImage)
        saveButton.clicked.connect(self.saveImage)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Text:"), self.lineEdit)
        formLayout.addRow(self.tr("&Font:"), self.fontComboBox)
        formLayout.addRow(self.tr("Font &Size:"), self.sizeSpinBox)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 3, Qt.AlignCenter)
        layout.addLayout(formLayout, 1, 0, 1, 3)
        layout.addWidget(saveButton, 2, 1)
        self.setLayout(layout)

        self.updateImage()
        self.setWindowTitle(self.tr("Paint Text"))

    def updateImage(self):

        font = QFont(self.fontComboBox.currentFont())
        font.setPointSizeF(self.sizeSpinBox.value())
        metrics = QFontMetricsF(font)

        text = unicode(self.lineEdit.text())
        if not text:
            return

        rect = metrics.boundingRect(text)
        position = -rect.topLeft()

        pixmap = QPixmap(rect.width(), rect.height())
        pixmap.fill(Qt.white)

        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(font)
        painter.drawText(position, text)
        painter.end()

        self.label.setPixmap(pixmap)

    def saveImage(self):

        formats = QImageWriter.supportedImageFormats()
        formats = map(lambda suffix: u"*." + unicode(suffix), formats)
        path = unicode(QFileDialog.getSaveFileName(self, self.tr("Save Image"),
                                                   "", self.tr("Image files (%1)").arg(u" ".join(formats))))

        if path:
            if not self.label.pixmap().save(path):
                QMessageBox.warning(self, self.tr("Save Image"),
                                    self.tr("Failed to save file at the specified location."))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

'''
class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.text = "test"

        self.setGeometry(300, 300, 280, 170)
        self.counter = 0
        self.show()
        self.showMaximized()

    def paintEvent(self, event):
        print "llega ", self.counter
        self.counter += 1
        image = QtGui.QImage("../assets/headset.png")
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.drawImage(QtCore.QPoint(0, 0), image)
        painter.setBrush(QtGui.QColor(102, 175, 54))
        painter.drawEllipse(82, 57, 28, 28)
        painter.drawEllipse(221, 57, 28, 28)

        painter.drawEllipse(35, 104, 28, 28)
        painter.drawEllipse(114, 107, 28, 28)
        painter.drawEllipse(190, 107, 28, 28)
        painter.drawEllipse(269, 104, 28, 28)

        painter.drawEllipse(67, 149, 28, 28)
        painter.drawEllipse(236, 149, 28, 28)

        painter.drawEllipse(18, 197, 28, 28)
        painter.drawEllipse(286, 197, 28, 28)
        painter.end()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()'''