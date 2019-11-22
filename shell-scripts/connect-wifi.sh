#!/bin/bash
if [ -z $1 ]; then
    >&2 echo "no ssid provided"
    exit 1
fi

SSID=$1
PSK="psk=\"$2\""

# If no password provided, set key_mgmt to NONE
if [ -z $2 ]; then
    PSK="key_mgmt=NONE"
fi

if [[ $(grep $SSID /etc/wpa_supplicant/wpa_supplicant.conf) ]]; then
    # SSID already exists in configuration, so just change password
    sed "/$SSID/!b;n;c\	$PSK" /etc/wpa_supplicant/wpa_supplicant.conf | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf
else
    # Create new configuration entry
    printf "\nnetwork={\n\tssid=\"$SSID\"\n\t$PSK\n}" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
fi

sudo service dhcpcd restart

sleep 5

# Reconfigure interface
wpa_cli -i wlan0 reconfigure

CONNECTED=0

# Check if connected to network for a max of 30 seconds
for i in {1..30}
do
    sleep 1
    if [ -n "$(iwgetid | sed "s/^.*ESSID:\"\(.*\)\"/\1/g")" ]; then
        CONNECTED=1
        break
    fi
done

# If connection is unsuccessful, then reconfigure access point
if [ $CONNECTED -eq 0 ]; then
    >&2 echo "failed to connect to $SSID"
    exit 1
fi

# Take down access point interface
sudo ifconfig uap0 down
iw dev uap0 del
sudo service dhcpcd restart

# Turn off AP software
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

exit 0
