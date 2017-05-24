import matplotlib.pyplot as plt
import time
import random
import numpy as np
import platform
import sys
import os

if platform.system() == "Windows":
    pass
from emokit.emotiv import Emotiv
from emokit.util import get_quality_scale_level_color

#xdata = [ [],[],[],[],[],[],[],[],[],[],[],[],[],[] ]
#ydata = [ [],[],[],[],[],[],[],[],[],[],[],[],[],[] ]
xdata = [ [], [] ]
ydata = [ [], [] ]
colors = ["#000000","#660033","#990099","#6600cc","#0000ff","#3399ff","#66ffff","#99ffcc","#ccffcc","#000099","#0066cc","#00cccc","#00ff80","#ff0000"]
#names = 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' ')
names = 'AF3 F7'.split(' ')
f, axarr = plt.subplots( len(xdata), sharex=True, sharey=True)
f, axarr2 = plt.subplots( len(xdata), sharex=True, sharey=True)

for ax in xrange(0,len(axarr)):
    axarr[ax].set_xlim(0, 100)
    axarr[ax].set_ylabel(names[ax])
    axarr2[ax].set_ylabel( names[ax] )
    axarr[ax].grid()
    axarr2[ax].grid()

def set_packet( packet ):
    for i in xrange(len(xdata)):
        xdata[i].append( len(xdata[i]) )
        ydata[i].append( packet.sensors[names[i]]['value'] )

def compute_fft(data):
	# Comput fft amplitude spectrum
	y = np.fft.fft(data)
	length_y = len(y)
	y_normalized = (y/float(length_y))*2.0;
	y_shifted = np.fft.fftshift(y_normalized)

	# Return the positive frequency components
	return np.absolute(y_shifted[0:(length_y/2)+1])

desp = 1
i = 0
updated = False

'''
with Emotiv(display_output=False, verbose=True ) as emotiv:
    while emotiv.running:
        try:
            packet = emotiv.dequeue()
            if packet is not None:
                updated = True
                i += 1
            time.sleep(0.001)

        except Exception as ex:
            print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                  " : ", ex)

        if updated:
            set_packet(packet)
            if plt.fignum_exists(1):
                if i > 100:
                    for axes in axarr:
                        axes.set_xlim(0 + desp, 100 + desp)
                        axes.pop(0)
                    desp += 1

                for ax in xrange(0, len(axarr)):
                    axarr[ax].plot(xdata[ax], ydata[ax], color=colors[ax])
                    npdata = np.array(xdata[ax])
                    sp = np.fft.fft(ydata[ax])
                    freq = np.fft.fftfreq(npdata.shape[-1])
                    axarr2[ax].plot(freq, sp.real, freq, sp.imag, color=colors[ax])
                plt.draw()
                plt.pause(1e-17)
                time.sleep(0.0001)
            else:
                break
'''

for i in xrange(1000):
    for x in xrange(0, len(xdata)):
        xdata[x].append(i)
        ydata[x].append(random.randint(0, 50))

    if plt.fignum_exists( 1 ):
        if i > 100:
            for axes in axarr:
                axes.set_xlim(0+desp, 100+desp)
            desp += 1

        for ax in xrange(0, len(axarr)):
            axarr[ax].plot(xdata[ax], ydata[ax], color=colors[ax])
            npdata = np.array(xdata[ax])
            sp = np.fft.fft(ydata[ax])
            freq = np.fft.fftfreq(npdata.shape[-1])
            axarr2[ax].plot(freq, sp.real, freq, sp.imag, color=colors[ax])
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.001)
    else:
        break

# add this if you don't want the window to disappear at the end
#plt.show()