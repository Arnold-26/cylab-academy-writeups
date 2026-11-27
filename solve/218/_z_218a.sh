#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== 218 file ==="
file 218_chall | cut -c1-120
echo "=== symbols ==="
nm 218_chall 2>/dev/null | head -30
echo "=== strings ==="
strings -n 5 218_chall | grep -vE '^(GCC|GLIBC|__|\.)' | head -25
