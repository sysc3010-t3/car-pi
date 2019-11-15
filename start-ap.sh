sed -e "/^.*#.*interface\swlan0/,/^.*#.*nohook\swpa_supplicant/ s/^#\(.*\)$/\1/g" /etc/dhcpcd.conf | sudo tee /etc/dhcpcd.conf
sudo service dhcpcd restart

sleep 1

sudo systemctl start hostapd
sudo systemctl start dnsmasq
