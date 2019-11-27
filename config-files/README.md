# Raspberry Pi Network Configuration
The files in this folder configure the network settings of the Raspberry Pi to
allow for the Pi to act as an access point as well as connect to a WiFi network.

The following are the locations for each file:
* `dhcpcd.conf` -> `/etc/dhcpcd.conf`
* `dnsmasq.conf` -> `/etc/dnsmasq.conf`
* `hostapd` -> `/etc/default/hostapd`
* `hostapd.conf` -> `/etc/hostapd/hostapd.conf`
* `iptables.ipv4.nat` -> `/etc/iptables.ipv4.nat`
* `rc.local` -> `/etc/rc.local`
* `wifistart` -> `/usr/local/bin/wifistart`

After the files are in the proper locations, reboot the Raspberry Pi for the
changes to take place.
