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
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.leftPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TAB_TRAVERSAL )
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.captureButton = wx.Button( self.leftPanel, wx.ID_ANY, u"Capture", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.captureButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.openButton = wx.Button( self.leftPanel, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer19.Add( self.openButton, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.leftPanel.SetSizer( bSizer19 )
		self.leftPanel.Layout()
		bSizer18.Add( self.leftPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.rightPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 700,-1 ), wx.TAB_TRAVERSAL )
		bSizer18.Add( self.rightPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer18 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.captureButton.Bind( wx.EVT_BUTTON, self.CaptureAction )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def CaptureAction( self, event ):
		event.Skip()
	

