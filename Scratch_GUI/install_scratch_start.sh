#! /bin/bash
# Copyright Dexter Industries, 2015.
# Install the Scratch GUI.
# Dev Notes:
# Helpful Link on Bin Paths:  http://www.cyberciti.biz/faq/how-do-i-find-the-path-to-a-command-file/

sudo apt-get --purge remove python-wxgtk2.8 python-wxtools wx2.8-i18n
sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n --force-yes
sudo apt-get install python-psutil --force-yes
sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n --force-yes

# Copy shortcut to desktop.
cp /home/pi/Desktop/DexterEd/Scratch_GUI/Scratch_Start.desktop /home/pi/Desktop
# Make shortcut executable
sudo chmod +x /home/pi/Desktop/Scratch_Start.desktop
# Make run_scratch_gui executable.
sudo chmod +x /home/pi/Desktop/DexterEd/Scratch_GUI/Scratch_Start.sh
# Make scratch start example read only.
sudo chmod ugo+r /home/pi/Desktop/DexterEd/Scratch_GUI/new.sb	# user, group, etc are just read only
# Make select_state readable and writale
sudo chmod 777 /home/pi/Desktop/DexterEd/Scratch_GUI/selected_state

# Remove Scratch Shortcuts if they're there.
sudo rm /home/pi/Desktop/BrickPi_Scratch_Start.desktop
sudo rm /home/pi/Desktop/GoPiGo_Scratch_Start.desktop
sudo rm /home/pi/Desktop/scratch.desktop

# Make sure that Scratch always starts Scratch GUI
# We'll install these parts to make sure that if a user double-clicks on a file on the desktop
# Scratch GUI is launched, and all other programs are killed.

#delete scratch from /usr/bin
sudo rm /usr/bin/scratch
# make a new scratch in /usr/bin
sudo cp /home/pi/Desktop/DexterEd/Scratch_GUI/scratch /usr/bin
# Change scratch permissions
sudo chmod +x /usr/bin/scratch

# set permissions
# sudo chmod +x /home/pi/Desktop/DexterEd/Scratch_GUI/scratch_launch
sudo chmod +x /home/pi/Desktop/DexterEd/Scratch_GUI/scratch_direct
