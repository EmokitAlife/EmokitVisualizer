""" ps_QPainter_drawRect101.py
explore the PySide GUI toolkit to draw rectangles in different colors
there are a number of ways colors can be specified
fill colors are set with the brush
perimeter colors are set with the pen
QColor can be given a transparency value
(PySide is the official LGPL-licensed version of PyQT)
for Python33 you can use the Windows self-extracting installer
PySide-1.1.2.win32-py3.3.exe
(PyQT483 equivalent) from:
http://qt-project.org/wiki/PySide
or:
http://www.lfd.uci.edu/~gohlke/pythonlibs/
for Qpainter methods see:
http://srinikom.github.com/pyside-docs/PySide/QtGui/
QPainter.html?highlight=qpainter#PySide.QtGui.PySide.QtGui.QPainter
tested with Python27 and Python33 by  vegaseat  14jan2013
"""
from PySide.QtCore import *
from PySide.QtGui import *
class MyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # setGeometry(x_pos, y_pos, width, height)
        # upper left corner coordinates (x_pos, y_pos)
        self.setGeometry(300, 300, 370, 100)
        self.setWindowTitle('Colors set with brush and pen')
    def paintEvent(self, e):
        '''
        the method paintEvent() is called automatically
        the QPainter class does all the low-level drawing
        coded between its methods begin() and end()
        '''
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    def drawRectangles(self, qp):
        '''use QPainter (instance qp) methods to do drawings'''
        # there are several different ways to reference colors
        # use HTML style color string #RRGGBB with values 00 to FF
        black = "#000000"
        # QPen(color, width, style)
        qp.setPen(black)
        # use QColor(r, g, b) with values 0 to 255
        qp.setBrush(QColor(255, 0, 0))
        # drawRect(int x, int y, int width, int height)
        # upper left corner coordinates (x, y)
        qp.drawRect(10, 15, 90, 60)
        # there are some preset named colors
        qp.setBrush(QColor(Qt.green))
        qp.drawRect(160, 25, 90, 60)
        # this rectangle will overlap the previous one
        # you can give it some transparency alpha 0 to 255
        # QColor(int r, int g, int b, int alpha=255)
        qp.setBrush(QColor(0, 0, 255, 100))
        qp.drawRect(130, 15, 90, 60)
        # some colors can be given as strings
        qp.setBrush(QColor('yellow'))
        qp.drawRect(265, 25, 90, 60)
app = QApplication([])
win = MyWindow()
win.show()
# run the application event loop
app.exec_()