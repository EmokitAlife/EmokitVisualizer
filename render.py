#!/usr/bin/python
# Renders a window with graph values for each sensor and a box for gyro values.
try:
    import psyco
    psyco.full()
except ImportError:
    print('')
import platform
import sys
import os
import time
import datetime

import pygame
from pygame import FULLSCREEN

if platform.system() == "Windows":
    pass
from emokit.emotiv import Emotiv
from emokit.util import get_quality_scale_level_color


class Grapher(object):
    """
    Worker that draws a line for the sensor value.
    """

    def __init__(self, screen, name, i, old_model=False):
        """
        Initializes graph worker
        """
        self.screen = screen
        self.name = name
        self.range = float(1 << 13)
        self.x_offset = 40
        self.y = i * gheight
        self.buffer = []
        font = pygame.font.Font(None, 24)
        self.text = font.render(self.name, 1, (255, 0, 0))
        self.text_pos = self.text.get_rect()
        self.text_pos.centery = self.y + gheight
        self.first_packet = True
        self.y_offset = 0
        self.old_model = old_model

    def update(self, packet):
        """
        Appends value and quality values to drawing buffer.
        """
        if len(self.buffer) == 800 - self.x_offset:
            self.buffer = self.buffer[1:]
        self.buffer.append([packet.sensors[self.name]['value'], packet.sensors[self.name]['quality']])

    def calc_y(self, val):
        """
        Calculates line height from value.
        """
        return val - self.y_offset + gheight

    def draw(self):
        """
        Draws a line from values stored in buffer.
        """
        if len(self.buffer) == 0:
            return

        if self.first_packet:
            self.y_offset = self.buffer[0][0]
            self.first_packet = False
        pos = self.x_offset, self.calc_y(self.buffer[0][0]) + self.y
        for i, (value, quality) in enumerate(self.buffer):
            y = self.calc_y(value) + self.y
            if self.old_model:
                color = str(get_quality_scale_level_color(quality, True))
            else:
                color = str(get_quality_scale_level_color(quality, False))
            pygame.draw.line(self.screen, (10,20,30), pos, (self.x_offset + i, y))
            pos = (self.x_offset + i, y)
        self.screen.blit(self.text, self.text_pos)

def save_recordings( recordings, file_name, header_text ):
    for record in recordings:
        file_name += datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S') + ".csv"
        output_file = open(file_name, 'w')
        output_file.write(header_text + "\n")
        for packet in record:
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

class PacketLine:

    def __init__(self, line):
        self.sensors = {}
        self.timestamp = time.mktime(datetime.datetime.strptime( line[0], "%Y-%m-%d %H:%M:%S.%f").timetuple())
        index = 1

        for name in 'F3 FC5 F7 T7 P7 O1 O2 P8 T8 F8 AF4 FC6 F4 AF3'.split(' '):
            self.sensors[name] = {}
            if line[index] == '?': self.sensors[name]['value'] = line[index]
            else: self.sensors[name]['value'] = int(line[index])

            if line[index+1] == '?': self.sensors[name]['quality'] = line[index+1]
            else: self.sensors[name]['quality'] = int(line[index+1])

            index += 2

        self.sensors['X'] = {}
        if line[index] == '?': self.sensors['X']['value'] = line[index]
        else: self.sensors['X']['value'] = int(line[index])

        self.sensors['Y'] = {}
        if line[index+1] == '?': self.sensors['Y']['value'] = line[index+1]
        else: self.sensors['Y']['value'] = int(line[index+1])

        self.sensors['Z'] = {}
        if line[index+2] == '?': self.sensors['Z']['value'] = line[index+2]
        else: self.sensors['Z']['value'] = int(line[index+2])

def main():
    """
    Creates pygame window and graph drawing workers for each sensor.
    """
    global gheight
    graphers = []
    recordings = []
    recording = False
    record_packets = []
    updated = False
    cursor_x, cursor_y = 400, 300
    fullscreen = False
    file_name = "output_data_";
    header_text = "Timestamp,F3 Value,F3 Quality,FC5 Value,FC5 Quality,F7 Value,F7 Quality,T7 Value,T7 Quality,P7 Value,P7 Quality,O1 Value,O1 Quality,O2 Value,O2 Quality,P8 Value,P8 Quality,T8 Value,T8 Quality,F8 Value,F8 Quality,AF4 Value,AF4 Quality,FC6 Value,FC6 Quality,F4 Value,F4 Quality,AF3 Value,AF3 Quality,X Value,Y Value,Z Value"
    default_line = [ "", '0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0','0', '0', '0']

    print "Ingrese opcion:"
    opcion = int(sys.stdin.readline().strip())

    if opcion == 1:
        file_name = sys.stdin.readline().strip()
        #read_file = open( file_name, 'r' )
        with open(file_name, 'r') as file:
            lines = file.readlines()

            pygame.init()
            screen = pygame.display.set_mode((800, 600))

            for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' '):
                graphers.append( Grapher(screen, name, len(graphers) ) )

            packets_in_queue = 0
            lines.pop(0)
            #for line in lines:
            while True:
                if( len(lines) != 0 ):
                    line = lines.pop(0).strip().split(",")
                else:
                    line =default_line
                    line[0] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                try:
                    while packets_in_queue < 8:
                       packet = PacketLine(line)
                       if packet is not None:
                           #print packet.sensors
                           if abs(packet.sensors['X']['value']) > 1:
                               cursor_x = max(0, min(cursor_x, 800))
                               cursor_x -= packet.sensors['X']['value']
                           if abs(packet.sensors['Y']['value']) > 1:
                               cursor_y += packet.sensors['Y']['value']
                               cursor_y = max(0, min(cursor_y, 600))
                           map(lambda x: x.update(packet), graphers)
                           if recording:
                               record_packets.append(packet)
                           updated = True
                           packets_in_queue += 1
                       time.sleep(0.001)
                except Exception as ex:
                    print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                                   " : ", ex)

                if updated:
                    screen.fill((75, 75, 75))
                    map(lambda x: x.draw(), graphers)
                    pygame.draw.rect(screen, (255, 255, 255), (cursor_x - 5, cursor_y - 5, 10, 10), 0)
                    pygame.display.flip()
                    updated = False
    else:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        with Emotiv(display_output=False, verbose=True ) as emotiv:
            for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' '):
                graphers.append(Grapher(screen, name, len(graphers), emotiv.old_model))
            while emotiv.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save_recordings(recordings, file_name, header_text)
                        emotiv.stop()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            save_recordings(recordings, file_name, header_text)
                            emotiv.stop()
                            return
                        elif event.key == pygame.K_f:
                            if fullscreen:
                                screen = pygame.display.set_mode((800, 600))
                                fullscreen = False
                            else:
                                screen = pygame.display.set_mode((800, 600), FULLSCREEN, 16)
                                fullscreen = True
                        elif event.key == pygame.K_r:
                            if not recording:
                                record_packets = []
                                recording = True
                            else:
                                recording = False
                                recordings.append(list(record_packets))
                                record_packets = None
                packets_in_queue = 0
                try:
                    while packets_in_queue < 8:
                        packet = emotiv.dequeue()
                        if packet is not None:
                            #print packet.sensors
                            if abs(packet.sensors['X']['value']) > 1:
                                cursor_x = max(0, min(cursor_x, 800))
                                cursor_x -= packet.sensors['X']['value']
                            if abs(packet.sensors['Y']['value']) > 1:
                                cursor_y += packet.sensors['Y']['value']
                                cursor_y = max(0, min(cursor_y, 600))
                            map(lambda x: x.update(packet), graphers)
                            if recording:
                                record_packets.append(packet)
                            updated = True
                            packets_in_queue += 1
                        time.sleep(0.001)
                except Exception as ex:
                    print("EmotivRender DequeuePlotError ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],
                          " : ", ex)
                if updated:
                    screen.fill((75, 75, 75))
                    map(lambda x: x.draw(), graphers)
                    pygame.draw.rect(screen, (255, 255, 255), (cursor_x - 5, cursor_y - 5, 10, 10), 0)
                    pygame.display.flip()
                    updated = False

if __name__ == "__main__":
    try:
        gheight = 580 // 14
        main()
    except Exception as ex:
        print("EmotivRender ", sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2], " : ", ex)
