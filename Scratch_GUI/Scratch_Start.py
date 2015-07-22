import wx
import os
import pickle
from datetime import datetime
import subprocess
from collections import Counter
import threading
import psutil
import signal

# Commenting
# Test
# Space out commands.
# Executable

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
		start_programming = wx.Button(self, label="Start Programming", pos=(25,75))
		start_programming.Bind(wx.EVT_BUTTON, self.start_programming)
		
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
		dlg = wx.MessageDialog(self, 'This will close any open Scratch programs.  Please save and click Ok!', 'Alert!', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
		out, err = p.communicate()
		print out
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
		
		# Start Scratch
		start_command = "scratch /home/pi/Desktop/DexterEd/Scratch_GUI/new.sb"
		send_bash_command_in_background(start_command)
		'''
		dlg = wx.MessageDialog(self, 'Starting Scratch Programming!', 'Update', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		'''

	
	def curriculum_update(self, event):
		write_debug("Update pressed.")
		# app = wx.PySimpleApp()
		progressMax = 100
		dlg = wx.ProgressDialog("Update DexterEd", "Remaining", progressMax,style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
		print(os.path.isdir("/home/pi/Desktop/DexterEd/"))
		dlg.Update(25)
		if(os.path.isdir("/home/pi/Desktop/DexterEd")):
			dlg.Update(35)
			os.chdir("/home/pi/Desktop/DexterEd")
			send_bash_command("git fetch origin")
			dlg.Update(55)
			send_bash_command("git reset --hard")
			dlg.Update(65)
			send_bash_command("git merge origin/master")
			dlg.Update(75)
		else:
			os.chdir("/home/pi/Desktop/") 											# Change directory.
			dlg.Update(25)
			send_bash_command("git clone https://github.com/DexterInd/DexterEd")	# Clone the repo.
			dlg.Update(35)
		print "End of Dialog Box!"
		
		# Check Permissions of Scratch, Update them.
		print "Install Scratch Shortcuts and Permissions."
		send_bash_command("sudo rm /home/pi/Desktop/GoPiGo_Scratch_Start.desktop")  					# Delete old icons off desktop
		send_bash_command("sudo cp /home/pi/Desktop/GoPiGo/Software/Scratch/GoPiGo_Scratch_Scripts/GoPiGo_Scratch_Start.desktop /home/pi/Desktop")	# Move icons to desktop
		send_bash_command("sudo chmod +x /home/pi/Desktop/GoPiGo/Software/Scratch/GoPiGo_Scratch_Scripts/GoPiGoScratch_debug.sh")					# Change script permissions
		send_bash_command("sudo chmod +x /home/pi/Desktop/GoPiGo/Software/Scratch/GoPiGo_Scratch_Scripts/GoPiGo_Scratch_Start.sh")					# Change script permissions
		
		
		dlg.Destroy()
		
	def examples(self, event):
		write_debug("Examples Pressed.")	
		folder = read_state()
		directory = "nohup pcmanfm /home/pi/Desktop/"+folder+"/"
		send_bash_command_in_background(directory)
		print "Opened up file manager!"
		write_debug("Opened up file manager!")

	def About(self, event):
		write_debug("About Pressed.")	
		dlg = wx.MessageDialog(self, 'Learn more about Dexter Industries and DexterEd at dexterindustries.com', 'About', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
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

		wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
		wx.Log.SetVerbose(False)
		wx.Frame.__init__(self, None, title="Scratch for Robots", size=(400,600))		# Set the fram size

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