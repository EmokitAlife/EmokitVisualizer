# -*- coding: utf-8 -*-
# This is adds a pyqtgraph gui to the data coming from the headset


import time
from emokit.emotiv import Emotiv
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

electrodes = (('AF3', (15, 150, 255)), ('AF4', (150, 255, 15)), ('F3', (255, 15, 150)), ('F4', (15, 150, 255)), ('F7', (150, 255, 15)), ('F8', (255, 15, 150)),
              ('FC5', (15, 150, 255)), ('FC6', (150, 255, 15)), ('T7', (255, 15, 150)), ('T8', (15, 150, 255)), ('P7', (150, 255, 15)), ('P8', (255, 15, 150)),
              ('O1', (15, 150, 255)), ('O2', (150, 255, 15))
              )

win = pg.GraphicsWindow()
win.setWindowTitle('Emo-Viewer')

# Plot in chunks, adding one new plot curve for every 100 samples
chunkSize = 100
# Remove chunks after we have 10
maxChunks = 10
startTime = pg.ptime.time()

headset = Emotiv()

allWaves = []
for i in xrange(14):
    if i:
        win.nextRow()
    p = win.addPlot()
    # p.setPen((255, 125, 123))
    if i == 13:
        p.setLabel('bottom', 'Time', 's')
    else:
        p.showAxis('bottom', False)
    # p.setXRange(-10, 0)
    curves = []
    data = np.empty((chunkSize + 1, 2))
    ptr = 0
    allWaves.append([p, data, ptr, curves])


def update3(p, data, ptr, i_curves, startTime, emo_data, color):
    now = pg.ptime.time()
    for c in i_curves:
        c.setPos(-(now - startTime), 0)

    i = ptr % chunkSize
    if i == 0:
        curve = p.plot()
        curve.setPen(color)  # (255, 125, 123))
        i_curves.append(curve)
        last = data[-1]
        data = np.empty((chunkSize + 1, 2))
        data[0] = last
        while len(i_curves) > maxChunks:
            c = i_curves.pop(0)
            p.removeItem(c)
    else:
        curve = i_curves[-1]
    data[i + 1, 0] = now - startTime
    data[i + 1, 1] = emo_data / 4000  #np.random.normal()  # dummy data  #
    # print emo_data
    # data[i + 1, 1] = ef.process_decrypted_packet_queue(raw_decrypted_packet, processed_packets)
    curve.setData(x=data[:i + 2, 0], y=data[:i + 2, 1])
    ptr += 1
    return [p, data, ptr, i_curves]


# update all plots
def update():
    global allWaves
    global startTime
    global headset
    packet = headset.dequeue()
    #print packet
    #packet = 1
    if packet is not None:
        for i, wave in enumerate(allWaves):
            wave = update3(*wave, startTime=startTime, emo_data=packet.sensors[electrodes[i][0]]['value'], color=electrodes[i][1])
            #wave = update3(*wave, emo_data=1, color=electrodes[i][1])
            allWaves[i] = wave


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

'''
if __name__ == "__main__":
    with Emotiv(display_output=False, verbose=False) as headset:
        while True:
            packet = headset.dequeue()
            if packet is not None:
                # pass
            time.sleep(0.1)
'''
