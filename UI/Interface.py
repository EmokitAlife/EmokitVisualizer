# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pyqtgraph as pg
from PySide.QtGui import *
from Record import Record
from FromFile import FromFile

class Interface ( QTabWidget ):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

        self.recordTab = Record()
        self.fromFileTab = FromFile()

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")

        self.tab1UI()
        self.tab2UI()
        self.setWindowTitle("Emokit Visualizer")
        self.showMaximized()

    def tab1UI(self):
        self.setTabText(0, "Grabar")
        self.tab1.setLayout( self.recordTab.setRecordTab() )

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.recordTab.update)
        self.timer.start(10)

    def tab2UI(self):
        self.setTabText(1, "Desde archivo")
        self.tab2.setLayout( self.fromFileTab.setFromFileTab() )

def main():
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()