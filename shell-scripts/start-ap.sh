iw dev wlan0 interface add uap0 type __ap
sudo ifconfig uap0 up
sudo service dhcpcd restart

sleep 1

sudo systemctl start hostapd
sudo systemctl start dnsmasq
