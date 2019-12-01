#!/bin/bash

# Take down access point interface
sudo ifconfig uap0 down
sudo iw dev uap0 del
sudo service dhcpcd restart

# Wait 5 seconds in case of any race conditions
sleep 5

# Turn off AP software
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

sleep 10
