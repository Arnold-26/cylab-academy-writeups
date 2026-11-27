#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 276_keygenme
echo "=== file ==="
file 276_keygenme | cut -c1-110
echo "=== strings ==="
strings -n 5 276_keygenme | grep -viE '^(GCC|GLIBC|__|_|\.)' | head -25
echo "=== symbols ==="
nm 276_keygenme 2>/dev/null | grep -E ' T ' | head -15
echo "=== run ==="
timeout 10 ./276_keygenme 2>&1 | head -5
