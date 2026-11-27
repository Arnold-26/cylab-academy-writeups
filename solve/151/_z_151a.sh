#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 151_remote
file 151_remote | cut -c1-110
echo "=== execution ==="
printf 'test\n' | timeout 5 ./151_remote 2>&1 | head -5
echo "=== chaines ==="
strings -n 4 151_remote | grep -aiE "flag|pass|correct|wrong|enter|academy" | head -12
echo "=== import / symboles ==="
nm 151_remote 2>/dev/null | grep -E " [Tt] " | head -12
