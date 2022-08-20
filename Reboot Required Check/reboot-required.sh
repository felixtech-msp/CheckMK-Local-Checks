#!/bin/bash

if [ -f "/var/run/reboot-required" ]; then
    echo "1 \"System Reboot required\" - A system reboot is required."
else
    echo "0 \"System Reboot required\" - A system reboot is not required."
fi
