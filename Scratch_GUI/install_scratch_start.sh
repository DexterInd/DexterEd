#! /bin/bash
# Install the Scratch GUI.

# sudo apt-get install python-wxgtk2.8 python-wxtools wx2.8-i18n -y
# sudo apt-get install python-psutil -y

# Copy shortcut to desktop.
cp Scratch_Start.desktop /home/pi/Desktop
# Make shortcut executable
sudo chmod +x /home/pi/Desktop/Scratch_Start.desktop
# Make run_scratch_gui executable.
sudo chmod +x /home/pi/Desktop/DexterEd/Scratch_GUI/Scratch_Start.sh