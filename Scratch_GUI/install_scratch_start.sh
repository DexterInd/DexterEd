#! /bin/bash
# Install the Scratch GUI.

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
