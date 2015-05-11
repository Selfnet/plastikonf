plastikonf
==========

We at Selfnet/WH-Netz use plastikonf to automatically configure budget 
routers from TP-Link in order to sell them to our members to offer them 
wifi in dormitories where there isn't a fixed wifi installation.

#Dependencies (may be incomplete)
 * python3
 * python-pillow
 * python-pymongo
 * python-crypto
 * texlive
 * mongodb
 * netctl
 * espeak
 * pwgen
 * python-pyzmq
 
#How it works
Thanks to the barcodes on the router containing wifi MAC adress and initial WPA key 
scanning these barcodes collects enough information to connect to it. 
Plastikonf then generates random passwords for WPA key and admin 
password and chooses an ESSID by randomly picking a city from a list of 
(probably) all cities in the world. These are then merged into a custom 
base configuration. This configuration file then gets encrypted and is 
uploaded to the router's web interface. The router then reboots and 
plastikonf waits for it to become available with the new ESSID. 
Finally, plastikonf generates labels to be put on the router and its 
box. These are sent to a label printer (Brother QL-720NW) using a custom pure-python 
printer driver. (CUPS drivers weren't available back then).

The user is guided through the process by espeak-powered text-to-speech 
output. The user only has to scan the barcodes, confirm the chosen 
ESSID and put the labels on.

For supported models, see the code.

#How do I use?
 * run download-worldcitiespop.sh
 * Start mongodb
 * open a terminal multiplexer like tmux and launch
   * insert.py (inserts new devices into the db)
   * configurator.py (creates config and uploads to router)
   * finalizer.py (prints labels)
   * monitor.py (shows overall progress)
   * scan.py (while True: iwlist scan)
   * wifi-manager.py (as root, connects to wifi)
