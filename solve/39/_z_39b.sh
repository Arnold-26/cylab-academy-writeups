#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 39_need-for-speed
file 39_need-for-speed | cut -c1-110
echo "=== chaines ==="
strings -n 5 39_need-for-speed | grep -aviE "glibc|gcc|\.so|gnu" | head -20
echo "=== execution ==="
timeout 10 ./39_need-for-speed 2>&1 | head -10
echo "exit=$?"
