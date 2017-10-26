import UI.Frame as demo
import wx, sys, os, pygame
import threading
import time
import datetime

try:
    import psyco
    psyco.full()
except ImportError:
    print('No psyco. Expect poor performance. Not really...')

import platform
import sys
import time

import pygame
from pygame import FULLSCREEN

if platform.system() == "Windows":
    pass
from emokit.emotiv import Emotiv
from emokit.util import get_quality_scale_level_color


class CalcFrame(demo.MyFrame1):

    recording = False
    record_packets = []
    file_name = "output_data_";
    header_text = "Timestamp,F3 Value,F3 Quality,FC5 Value,FC5 Quality,F7 Value,F7 Quality,T7 Value,T7 Quality,P7 Value,P7 Quality,O1 Value,O1 Quality,O2 Value,O2 Quality,P8 Value,P8 Quality,T8 Value,T8 Quality,F8 Value,F8 Quality,AF4 Value,AF4 Quality,FC6 Value,FC6 Quality,F4 Value,F4 Quality,AF3 Value,AF3 Quality,X Value,Y Value,Z Value"

    def __init__(self, parent):
        demo.MyFrame1.__init__(self, parent)

        try:
            self.emotiv = Emotiv( display_output=False, verbose=True )
            print self.emotiv
            print self.emotiv.sensors
            print self.emotiv.running
        except Exception as ex:
            print ex
            # assert ( ex.message == "Device not found" )
        else:
            self.t = threading.Thread(target=self.hiloEmotiv)
            self.t.start()

    def grabarEvent(self, event):
        print "Captura!!!"

        self.recording = not self.recording

        if not self.recording:
            self.save_recordings()
            self.record_packets = []
            self.rec.Label = "Grabar"
        else:
            self.rec.Label = "Detener"

    def save_recordings(self):
        file_n = self.file_name + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S') + ".csv"
        output_file = open(file_n, 'w')
        output_file.write(self.header_text + "\n")
        for packet in self.record_packets:
            row_file = ""
            row_file += str(packet.timestamp) + ","
            row_file += str(packet.sensors['F3']['value']) + ","
            row_file += str(packet.sensors['F3']['quality']) + ","
            row_file += str(packet.sensors['FC5']['value']) + ","
            row_file += str(packet.sensors['FC5']['quality']) + ","
            row_file += str(packet.sensors['F7']['value']) + ","
            row_file += str(packet.sensors['F7']['quality']) + ","
            row_file += str(packet.sensors['T7']['value']) + ","
            row_file += str(packet.sensors['T7']['quality']) + ","
            row_file += str(packet.sensors['P7']['value']) + ","
            row_file += str(packet.sensors['P7']['quality']) + ","
            row_file += str(packet.sensors['O1']['value']) + ","
            row_file += str(packet.sensors['O1']['quality']) + ","
            row_file += str(packet.sensors['O2']['value']) + ","
            row_file += str(packet.sensors['O2']['quality']) + ","
            row_file += str(packet.sensors['P8']['value']) + ","
            row_file += str(packet.sensors['P8']['quality']) + ","
            row_file += str(packet.sensors['T8']['value']) + ","
            row_file += str(packet.sensors['T8']['quality']) + ","
            row_file += str(packet.sensors['F8']['value']) + ","
            row_file += str(packet.sensors['F8']['quality']) + ","
            row_file += str(packet.sensors['AF4']['value']) + ","
            row_file += str(packet.sensors['AF4']['quality']) + ","
            row_file += str(packet.sensors['FC6']['value']) + ","
            row_file += str(packet.sensors['FC6']['quality']) + ","
            row_file += str(packet.sensors['F4']['value']) + ","
            row_file += str(packet.sensors['F4']['quality']) + ","
            row_file += str(packet.sensors['AF3']['value']) + ","
            row_file += str(packet.sensors['AF3']['quality']) + ","
            row_file += str(packet.sensors['X']['value']) + ","
            row_file += str(packet.sensors['Y']['value']) + ","
            row_file += str(packet.sensors['Z']['value'])
            output_file.write(row_file + "\n")
        output_file.close()

        file_n = self.file_name + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S') + ".in"
        output_file = open( file_n, 'w')
        for packet in self.record_packets:
            for sensor in packet.sensors:
                if sensor != "X" and sensor != "Y" and sensor != "Z" and sensor != "Unknown":
                    row_file = ""
                    row_file += sensor + " " + str(packet.sensors[sensor]['value'])
                    output_file.write(row_file + "\n")
        output_file.close()

    def hiloEmotiv(self):
        while self.emotiv.running:
            try:
                packet = self.emotiv.dequeue()
                if packet is not None:
                    if self.recording:
                        self.record_packets.append(packet)
                    updated = True
                time.sleep(0.001)

            except Exception as ex:
                print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                      " : ", ex)


app = wx.App(False)
frame = CalcFrame(None)
frame.Show(True)
app.MainLoop()