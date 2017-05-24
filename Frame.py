# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(108, 71), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.rec = wx.Button(self, wx.ID_ANY, u"Grabar", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.rec, 0, wx.ALL, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.rec.Bind(wx.EVT_BUTTON, self.grabarEvent)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def grabarEvent(self, event):
        event.Skip()


