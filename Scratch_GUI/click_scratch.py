import wx
import os
import sys
import pickle
from datetime import datetime
import subprocess
from collections import Counter
import threading
import psutil
import signal

#	This program runs when a Scratch program is clicked on the desktop.
#	It should be called by a modified script in /usr/bin/scratch to start.
#	It will:
# 		- First allow a user to specify which platform they want to run (GrovePi, GoPiGo, or BrickPi)
#		- Second kill all Scratch programs.
#		- Third start the appropriate background program (GrovePi, GoPiGo, BrickPi)
# 		- Kill itself.
#	After the program is run, /usr/bin/scratch will start Scratch, opening the file.

# References
# http://www.blog.pythonlibrary.org/2010/03/18/wxpython-putting-a-background-image-on-a-panel/
# ComboBoxes!  		http://wiki.wxpython.org/AnotherTutorial#wx.ComboBox
# dfu-programmer:  	http://dfu-programmer.github.io/

# Writes debug to file "error_log"
def write_debug(in_string):
	# In in time logging.
	#print in_string
	write_string = str(datetime.now()) + " - " + in_string + "\n"
	error_file = open('error_log', 'a')		# File: Error logging
	error_file.write(write_string)
	error_file.close()

def write_state(in_string):
	error_file = open('selected_state', 'w')		# File: selected state
	error_file.write(in_string)
	error_file.close()

def read_state():
	error_file = open('selected_state', 'r')		# File: selected state
	in_string = ""
	in_string = error_file.read()
	error_file.close()
	return in_string
	
def send_bash_command(bashCommand):
	# print bashCommand
	write_debug(bashCommand)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) #, stderr=subprocess.PIPE)
	# print process
	output = process.communicate()[0]
	# print output
	return output

def send_bash_command_in_background(bashCommand):
	# Fire off a bash command and forget about it.
	write_debug(bashCommand)
	process = subprocess.Popen(bashCommand.split())

########################################################################
class MainPanel(wx.Panel):
	""""""
	#----------------------------------------------------------------------
	def __init__(self, parent):
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.frame = parent
 
		sizer = wx.BoxSizer(wx.VERTICAL)
		hSizer = wx.BoxSizer(wx.HORIZONTAL)
 
		
		#-------------------------------------------------------------------
		# Standard Buttons

		# Start Programming
		start_programming = wx.Button(self, label="Start Programming!", pos=(25,75))
		start_programming.Bind(wx.EVT_BUTTON, self.start_programming)
		
		'''
		# Open Examples
		examples_button = wx.Button(self, label="Open Examples", pos=(25, 125))
		examples_button.Bind(wx.EVT_BUTTON, self.examples)			
		
		# Update Curriculum
		curriculum_update = wx.Button(self, label="Update DexterEd", pos=(25,175))
		curriculum_update.Bind(wx.EVT_BUTTON, self.curriculum_update)

		# About
		about_button = wx.Button(self, label="About", pos=(25, 225))
		about_button.Bind(wx.EVT_BUTTON, self.About)		
		
		# Exit
		exit_button = wx.Button(self, label="Exit", pos=(25,275))
		exit_button.Bind(wx.EVT_BUTTON, self.onClose)
		'''

		# End Standard Buttons		
		#-------------------------------------------------------------------
		# Drop Boxes

		controls = ['GoPiGo', 'GrovePi', 'BrickPi']	# Options for drop down.

		# Select Platform.
		
		robotDrop = wx.ComboBox(self, -1, "GoPiGo", pos=(25, 25), size=(150, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		robotDrop.Bind(wx.EVT_COMBOBOX, self.robotDrop)					# Binds drop down.		
		wx.StaticText(self, -1, "Select a Robot:", (25, 5))					# (Minus 50, minus 0)
		
		# Drop Boxes
		#-------------------------------------------------------------------
		
		hSizer.Add((1,1), 1, wx.EXPAND)
		hSizer.Add(sizer, 0, wx.TOP, 100)
		hSizer.Add((1,1), 0, wx.ALL, 75)
		self.SetSizer(hSizer)
	
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)		# Sets background picture
 
	#----------------------------------------------------------------------
	def OnEraseBackground(self, evt):
		"""
		Add a picture to the background
		"""
		# yanked from ColourDB.py
		dc = evt.GetDC()
 
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		dc.Clear()	
		bmp = wx.Bitmap("/home/pi/Desktop/DexterEd/Scratch_GUI/dex.png")	# Draw the photograph.
		dc.DrawBitmap(bmp, 0, 400)						# Absolute position of where to put the picture
		
		# Add a second picture.
		robot = "/home/pi/Desktop/DexterEd/Scratch_GUI/"+read_state()+".png"
		bmp = wx.Bitmap(robot)	# Draw the photograph.
		dc.DrawBitmap(bmp, 200, 0)	

		
		
	def robotDrop(self, event):
		write_debug("robotDrop Selected.")
		controls = ['GoPiGo', 'GrovePi', 'BrickPi']	# Options for drop down.
		value = event.GetSelection()
		print controls[value]
		# position = 0					# Position in the key list on file
		write_state(controls[value]) 	# print value to file.  
		
		# Update Picture
		robot = "/home/pi/Desktop/DexterEd/Scratch_GUI/"+read_state()+".png"
		png = wx.Image(robot, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		wx.StaticBitmap(self, -1, png, (200, 0), (png.GetWidth(), png.GetHeight()))

	def start_programming(self, event):
		# Kill all Python Programs.  Any running *Scratch* Python Programs.
		write_debug("Start robot.")	
		dlg = wx.MessageDialog(self, 'This will close any open Scratch programs.  Please save your work and click Ok!', 'Alert!', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		out, err = p.communicate()
		# print out
		for line in out.splitlines():
			if 'squeakvm' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)
			if 'BrickPiScratch_' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)
			if 'GoPiGoScratch_d' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)
			if 'GrovePiScratch_d' in line:
				pid = int(line.split(None, 1)[0])
				os.kill(pid, signal.SIGKILL)

		folder = read_state()
		if folder == 'BrickPi':
			program = "/home/pi/Desktop/BrickPi_Scratch/BrickPiScratch.py"
		if folder == 'GoPiGo':
			program = "/home/pi/Desktop/GoPiGo/Software/Scratch/GoPiGoScratch.py"
		if folder == 'GrovePi':
			program = "/home/pi/Desktop/GrovePi/Software/Scratch/GrovePiScratch.py"
		start_command = "sudo python "+program
		send_bash_command_in_background(start_command)
		
		write_debug("Programming Started.")	
		
		self.frame.Close()
		sys.exit()				# Exit!
		# Start Scratch
		''' 
		start_command = "scratch /home/pi/Desktop/DexterEd/Scratch_GUI/new.sb"
		send_bash_command_in_background(start_command)
		dlg = wx.MessageDialog(self, 'Starting Scratch Programming!', 'Update', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		'''
		
		
	def onClose(self, event):	# Close the entire program.
		write_debug("Close Pressed.")
		"""
		"""
		self.frame.Close()
  
########################################################################
class MainFrame(wx.Frame):
	""""""
	
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		# wx.ComboBox

		wx.Icon('/home/pi/Desktop/DexterEd/Scratch_GUI/favicon.ico', wx.BITMAP_TYPE_ICO)
		wx.Log.SetVerbose(False)
		wx.Frame.__init__(self, None, title="Scratch for Robots", size=(400,300))		# Set the frame size

		panel = MainPanel(self)        
		self.Center()
 
########################################################################
class Main(wx.App):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        """Constructor"""
        wx.App.__init__(self, redirect, filename)
        dlg = MainFrame()
        dlg.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
	write_debug(" # Program # started # !")
	write_state("GoPiGo")
	# reset_file()	#Reset the file every time we turn this program on.
	app = Main()
	app.MainLoop()