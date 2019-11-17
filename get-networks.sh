#!/bin/bash
sudo iwlist wlan0 scan | grep 'ESSID\|802.11' | sed 's/\(^.*ESSID:\)\|"\|\(\s*Version.\+$\)//g' | sed 's/^.*\//:/g' | sed -r '/\(^\s*$\)\|\(^.*:\)/d' | tr '\n' ',' | sed 's/,$//g' | sed 's/,:/:/g'
