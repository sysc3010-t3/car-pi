#!/bin/bash

if [ -n "$(iwgetid | sed "s/^.*ESSID:\"\(.*\)\"/\1/g")" ]; then
    exit 0
else
    exit 1
fi
