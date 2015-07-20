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

key_map_on_startup = ['17']*11#, '20', '20', '20', '20', '20', '20', '20', '20', '20', '20']		# This is the default list now.
key_map=['0','0','0','0','0','0','0','0','0','0','0']
map=['L1 L2','R1 R2','UP DOWN','RIGHT LEFT','TRI X','O SQR','JLX','JLY','JRX','JRY','Servo Speed']
total_inp=10

# Writes debug to file "error_log"
def write_debug(in_string):
	# In in time logging.
	#print in_string
	write_string = str(datetime.now()) + " - " + in_string + "\n"
	error_file = open('error_log', 'a')		# File: Error logging
	error_file.write(write_string)
	error_file.close()



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
 
		btn1 = wx.Button(self, label="Upload Firmware", pos=(245,500))
		btn1.Bind(wx.EVT_BUTTON, self.WriteFirmware)
		
		#-------------------------------------------------------------------
		# Standard Buttons

		# About
		about_button = wx.Button(self, label="About", pos=(370,500))
		about_button.Bind(wx.EVT_BUTTON, self.About)		
		
		# Exit
		exit_button = wx.Button(self, label="Exit", pos=(475,500))
		exit_button.Bind(wx.EVT_BUTTON, self.onClose)

		# End Standard Buttons		
		#-------------------------------------------------------------------
		
		#-------------------------------------------------------------------
		# Drop Boxes

		controls = ['Servo 1', 'Servo 2', 'Servo 3', 'Servo 4', 'Servo 5', 'Servo 6', 'Motor 1', 'Motor 2', 'Motor 3', 'Motor 4']	# Options for drop down.

		######################
		## Left Side Controls
		
		# Controller: L1 L2
		L1L2Drop = wx.ComboBox(self, -1, "default value1", pos=(70, 25), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		L1L2Drop.Bind(wx.EVT_COMBOBOX, self.L1L2_ComboBox)					# Binds drop down.		
		wx.StaticText(self, -1, "L1 L2", (70, 5))					# (Minus 50, minus 0)
		
		# Controller: UP DOWN
		UPDOWNDrop = wx.ComboBox(self, -1, "default value2", pos=(5, 100), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		UPDOWNDrop.Bind(wx.EVT_COMBOBOX, self.UPDOWN_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Up/Down", (5, 80))					# (Minus 50, minus 0)
		
		# Controller: RIGHT LEFT
		RIGHTLEFTDrop = wx.ComboBox(self, -1, "default value2", pos=(5, 200), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		RIGHTLEFTDrop.Bind(wx.EVT_COMBOBOX, self.RIGHTLEFT_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Right/Left", (5, 180))					# (Minus 50, minus 0)

		# Controller: JLX
		JLXDrop = wx.ComboBox(self, -1, "default value2", pos=(5, 320), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		JLXDrop.Bind(wx.EVT_COMBOBOX, self.JLX_ComboBox)					# Binds drop down.	
		wx.StaticText(self, -1, "Left Joystick L/R", (5, 300))					# (Minus 50, minus 0)		
		
		# Controller: JLY
		JLYDrop = wx.ComboBox(self, -1, "default value2", pos=(145, 440), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		JLYDrop.Bind(wx.EVT_COMBOBOX, self.JLY_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Left Joystick U/D", (50, 445))					# (Minus 50, minus 0)		
		
		######################
		## Right Side Controls

		# Controller: R1 R2
		R1R2Drop = wx.ComboBox(self, -1, "default value2", pos=(430, 25), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		R1R2Drop.Bind(wx.EVT_COMBOBOX, self.R1R2_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "R1 R2", (430, 5))					# (Minus 50, minus 0)
		
		# Controller: Triangle X
		TRIXDrop = wx.ComboBox(self, -1, "default value2", pos=(500, 100), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		TRIXDrop.Bind(wx.EVT_COMBOBOX, self.TRIX_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Triangle/X", (515, 80))					# (Minus 50, minus 0)
		
		# Controller: O Square
		OSQDrop = wx.ComboBox(self, -1, "default value2", pos=(505, 200), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		OSQDrop.Bind(wx.EVT_COMBOBOX, self.OSQ_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "O/Square", (528, 180))					# (Minus 50, minus 0)
		
		# Controller: JRX
		JRXDrop = wx.ComboBox(self, -1, "default value2", pos=(505, 320), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		JRXDrop.Bind(wx.EVT_COMBOBOX, self.JRX_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Right Joystick L/R", (485, 300))					# (Minus 50, minus 0)		
		
		# Controller: Joy Stick Right Side Y Axis (JRY)
		JRYDrop = wx.ComboBox(self, -1, "default value2", pos=(390, 440), size=(75, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		JRYDrop.Bind(wx.EVT_COMBOBOX, self.JRY_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Right Joystick U/D", (473, 445))					# (Minus 50, minus 0)		
		
		# Speed Control
		controls = ['1', '2', '3', '4', '5', '6', '7', '8', '9']	# Options for drop down.
		SpeedDrop = wx.ComboBox(self, -1, pos=(100, 500), size=(50, -1), choices=controls, style=wx.CB_READONLY)  # Drop down setup
		SpeedDrop.Bind(wx.EVT_COMBOBOX, self.ServoSpeed_ComboBox)					# Binds drop down.				
		wx.StaticText(self, -1, "Servo Speed", (30, 505))					# (Minus 50, minus 0)								
		
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
		bmp = wx.Bitmap("PS2_CONTROLLER_GRAPHIC_600-3.JPG")	# Draw the photoraph.
		dc.DrawBitmap(bmp, -110, -150)						# Absolute position of where to put the picture
	
	def WriteFirmware(self, event):
		# Here and now we write the firmware.
		write_debug("++++++++++++++++++++++++++++++++++++++++++++++++")
		write_debug("Write some firmware!")
		
		# Open dialog to wait.
		write_debug("Open dialog to wait while firmware written.")	
		dlg = wx.MessageDialog(self, 'Beginning to write firmware to the controller.', 'Writing Firmware.', wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP)
		dlg.ShowModal()
		
		copy_success = copy_map_from_file()  # This function returns 0 if succesful, something else if failure.  
		
		if copy_success == 1:		# Check to see if we returned anything but zero.  If we did, we had an error.
			# print "FAILED TO COPY!  EXIT WriteFirmware!"
			# Show a popup box for this.  And then exit.
			dlg.Destroy()
			dlg = wx.MessageDialog(self, 'Error writing: Found two buttons assigned to one controller.  Failed to write firmware.', 'Failed To Write Firmware.', wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP)
			dlg.ShowModal()			
			dlg.Destroy()
			return 0
		
		dfu_status = 0	## This variable is zero, and if everything is succesful, stays 0.  Reports back at the end the status.
		# Status 1 means that the device wasn't found.   
		# Status 2
		
		
		# Running the uploading sequence
		# Erase Device
		# os.system('dfu-programmer.exe atmega32u4 erase')
		p = subprocess.Popen("dfu-programmer atmega32u4 erase", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		out, err = p.communicate()
		p.wait()		
		debug_line = "\n" + str(datetime.now()) + " Try to erase " + out
		write_debug(debug_line)
		
		# Search for error: "no device present"
		error_string = "no device present"
		if(out.find(error_string) >= 0): 
			dfu_status = 1
		
		# Flash eeprom
		if(dfu_status < 1):
			# os.system('dfu-programmer.exe atmega32u4 flash-eeprom EEP_Dump.hex')
			p = subprocess.Popen("dfu-programmer.exe atmega32u4 flash-eeprom EEP_Dump.hex", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out, err = p.communicate()
			p.wait()
			debug_line = "\n" + str(datetime.now()) + " Try to flash eeprom " + out
			write_debug(debug_line)
			
			# Search for error: "Error opening the file"
			error_string = "Error opening the file"
			if(out.find(error_string) >= 0): 
				dfu_status = 2
		
		# Flash firmware
		if(dfu_status < 1):
			# os.system('dfu-programmer.exe atmega32u4 flash PS2_motorcontroller_2014_08_02.hex')
			p = subprocess.Popen("dfu-programmer.exe atmega32u4 flash PS2_5.hex", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out, err = p.communicate()
			p.wait()
			debug_line = "\n" + str(datetime.now()) + " Try to flash firmware. " + out
			write_debug(debug_line)		
			
			# Search for error: "Error opening the file"
			error_string = "Error opening the file"
			if(out.find(error_string) >= 0): 
				dfu_status = 3			
				
		# Reset the device
		if(dfu_status < 1):
			# os.system('dfu-programmer.exe atmega32u4 reset')
			p = subprocess.Popen("dfu-programmer.exe atmega32u4 reset", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out, err = p.communicate()
			debug_line = "\n" + str(datetime.now()) + " Try to reset device. " + out
			write_debug(debug_line)
		
		# Close dialog window since write is done. 
		dlg.Destroy()
	
		# Open results dialog.
		write_debug("Results dialog on firmware.")	
		write_debug("Dfu_status: " + str(dfu_status))
		error_string = "Finished. Firmware was uploaded successfully."
		if(dfu_status == 1):
			error_string = "ERROR! \nCould not find controller.  Try reconnecting and pressing reset button on controller."
		if(dfu_status == 2):
			error_string = "ERROR! \nCould not find EEPROM file.  Try re-running the program."			
		if(dfu_status == 3):
			error_string = "ERROR! \nCould not find firmware file.  Try re-running the program."				
		dlg = wx.MessageDialog(self, error_string, 'Finished.', wx.OK|wx.ICON_INFORMATION|wx.STAY_ON_TOP)
		dlg.ShowModal()
		
	'''def Button2(self, event):
		# Here and now we write the firmware.
		print "Do whatever it is that button 2 does."
	'''	
	def L1L2_ComboBox(self, event):
		write_debug("L1L2_ComboBox Selected.")
		value = event.GetSelection()
		#print item
		position = 0					# Position in the key list on file
		write_to_file(position, value) 	# print value to file.  

	def R1R2_ComboBox(self, event):
		write_debug("R1R2_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 1					# Position in the key list on file
		write_to_file(position, value) 	# print value to file.
	
	def UPDOWN_ComboBox(self, event):
		write_debug("UPDOWN_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 2					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 

	def RIGHTLEFT_ComboBox(self, event):
		write_debug("RIGHTLEFT_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 3					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 

	def TRIX_ComboBox(self, event):
		write_debug("TRIX_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 4					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 		

	def OSQ_ComboBox(self, event):
		write_debug("OSQ_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 5					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 	
		
	def JLX_ComboBox(self, event):
		write_debug("JLX_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 6					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 	
		
	def JLY_ComboBox(self, event):
		write_debug("JLY_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 7					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 		
	
	def JRX_ComboBox(self, event):
		write_debug("JRX_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 8					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 	
		
	def JRY_ComboBox(self, event):
		write_debug("JRY_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 9					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 	

	def ServoSpeed_ComboBox(self, event):
		write_debug("ServoSpeed_ComboBox Pressed.")
		value = event.GetSelection()
		#print item
		position = 10					# Position in the key list on file
		write_to_file(position, value) 	# print value to file. 			
		
	def About(self, event):
		write_debug("About Pressed.")	
		dlg = wx.MessageDialog(self, 'This software is written by Dexter Industires for use with the Tetrix PS2 Controller.  Find more information at www.dexterindustries.com/PS2', 'About', wx.OK|wx.ICON_INFORMATION)
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
		wx.Frame.__init__(self, None, size=(600,600))		# Set the fram size
		
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
	reset_file()	#Reset the file every time we turn this program on.
	app = Main()
	app.MainLoop()