#!/bin/bash

# Take down access point interface
sudo ifconfig uap0 down
iw dev uap0 del
sudo service dhcpcd restart

# Turn off AP software
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq
