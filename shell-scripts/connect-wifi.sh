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

if [[ $(sudo grep "$SSID" /etc/wpa_supplicant/wpa_supplicant.conf) ]]; then
    # SSID already exists in configuration, so just change password
    sudo sed -i '/'"$SSID"'/!b;n;c\	'"$PSK" /etc/wpa_supplicant/wpa_supplicant.conf
else
    # Create new configuration entry
    printf "\n\nnetwork={\n\tssid=\"$SSID\"\n\t$PSK\n}" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
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
    ./shell-scripts/check_connection.sh
    if [[ $? -eq 0 ]]; then
        CONNECTED=1
        break
    fi
done

if [ $CONNECTED -eq 0 ]; then
    >&2 echo "failed to connect to $SSID"
    exit 1
fi

exit 0
