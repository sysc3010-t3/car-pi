#!/bin/bash
if [ -n $1 ] && [ -n $2 ]; then
        SSID=$1
        PSK=$2

        if [[ $(grep $SSID /etc/wpa_supplicant/wpa_supplicant.conf) ]]; then
                sed "/$SSID/!b;n;cpsk=\"$PSK\"" /etc/wpa_supplicant/wpa_supplicant.conf | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf
        else
                printf "\nnetwork={\n\tssid=\"$SSID\"\n\tpsk=\"$PSK\"\n}" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf
        fi

        # Turn off AP software
        sudo systemctl stop hostapd
        sudo systemctl stop dnsmasq

        # Change dhcpcd configuration
        sed -e "/^.*[^#]*interface\swlan0/,/^.*[^#]*nohook\swpa_supplicant/ s/^.*$/#&/g" /etc/dhcpcd.conf | sudo tee /etc/dhcpcd.conf
        sudo service dhcpcd restart

        sleep 1

        # Reconfigure interface
        wpa_cli -i wlan0 reconfigure
fi
