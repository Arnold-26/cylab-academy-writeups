#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== soumission a 11287 ==="
timeout 60 nc -w 2 xebec.cylabacademy.net 11287 < 432_modified.jpg 2>&1 | tail -40
