import wx
import os
import pickle
from datetime import datetime
import subprocess
from collections import Counter
 
# Commenting
# Test
# Space out commands.
# Executable

# References
# http://www.blog.pythonlibrary.org/2010/03/18/wxpython-putting-a-background-image-on-a-panel/
# ComboBoxes!  		http://wiki.wxpython.org/AnotherTutorial#wx.ComboBox
# dfu-programmer:  	http://dfu-programmer.github.io/

# key_map_on_startup = ['17']*11#, '20', '20', '20', '20', '20', '20', '20', '20', '20', '20']		# This is the default list now.
# key_map=['0','0','0','0','0','0','0','0','0','0','0']
# map=['L1 L2','R1 R2','UP DOWN','RIGHT LEFT','TRI X','O SQR','JLX','JLY','JRX','JRY','Servo Speed']
# total_inp=10

# Writes debug to file "error_log"
def write_debug(in_string):
	# In in time logging.
	#print in_string
	write_string = str(datetime.now()) + " - " + in_string + "\n"
	error_file = open('error_log', 'a')		# File: Error logging
	error_file.write(write_string)
	error_file.close()


def send_bash_command(bashCommand):
	print bashCommand
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE) #, stderr=subprocess.PIPE)
	print process
	output = process.communicate()[0]
	print output
	return output

########################################################################
class MainPanel(wx.Panel):
	""""""
	#----------------------------------------------------------------------
	def __init__(self, parent):
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
		# self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
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
		
		#-------------------------------------------------------------------
		# Drop Boxes

		controls = ['GoPiGo', 'GrovePi', 'BrickPi']	# Options for drop down.
		
		######################
		## Left Side Controls
		
		# Controller: L1 L2
		
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
		bmp = wx.Bitmap("dex.jpg")	# Draw the photograph.
		dc.DrawBitmap(bmp, -75, -75, false)						# Absolute position of where to put the picture
	
	def robotDrop(self, event):
		write_debug("robotDrop Selected.")
		value = event.GetSelection()
		#print item
		position = 0					# Position in the key list on file
		write_to_file(position, value) 	# print value to file.  

	def start_programming(self, event):
		write_debug("Start robot.")	
		dlg = wx.MessageDialog(self, 'Starting Scratch Programming!', 'Update', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
	
	
	def examples(self, event):
		write_debug("Examples pressed.")
		# send_bash_command("ping -c 1 google.com")
		# Check for Directory on Desktop
		print(os.path.isdir("/home/pi/Desktop/Dexter_Ed"))
		if(os.path.isdir("/home/pi/Desktop/Dexter_Ed")):
			send_bash_command("(cd /home/pi/Desktop/DexterEd && git fetch origin)")
			send_bash_command("(cd /home/pi/Desktop/DexterEd && git reset --hard)")
			send_bash_command("(cd /home/pi/Desktop/DexterEd && git merge origin/master)")
			
		else:
			# send_bash_command("(cd /home/pi/Desktop && git clone https://github.com/DexterInd/DexterEd)")
			send_bash_command("cd /home/pi/Desktop")
			send_bash_command("git clone https://github.com/DexterInd/DexterEd")
		dlg = wx.MessageDialog(self, 'Open up examples folder.', 'Update', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()

		
	def curriculum_update(self, event):
		write_debug("Curriculum Pressed.")	
		dlg = wx.MessageDialog(self, 'Update Curriculum . . . ', 'Update', wx.OK|wx.ICON_INFORMATION)
		dlg = wx.MessageDialog(self, str(i), str(i))
		dlg.ShowModal()
		dlg.Destroy()

	def About(self, event):
		write_debug("About Pressed.")	
		dlg = wx.MessageDialog(self, 'Learn more about Dexter Industries and DexterEd at dexterindustries.com', 'About', wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		
	def onClose(self, event):	# Close the entire program.
		write_debug("Close Pressed.")
		""""""
		self.frame.Close()
  
########################################################################
class MainFrame(wx.Frame):
	""""""
	
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		# wx.ComboBox

		wx.Icon('favicon.ico', wx.BITMAP_TYPE_ICO)
		wx.Frame.__init__(self, None, size=(400,600))		# Set the fram size
		
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
	# reset_file()	#Reset the file every time we turn this program on.
	app = Main()
	app.MainLoop()