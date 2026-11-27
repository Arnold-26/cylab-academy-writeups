#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 133_gauntlet
file 133_gauntlet | cut -c1-110
echo "=== symboles ==="
nm 133_gauntlet 2>/dev/null | grep -E " [Tt] " | head -12
echo "=== main ==="
objdump -d -Mintel 133_gauntlet 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "call|lea|printf|fgets|strcpy|add +rsp" | head -20
echo "=== chaines ==="
strings -n 6 133_gauntlet | head -12
echo "=== GNU_STACK ==="
readelf -lW 133_gauntlet 2>/dev/null | grep GNU_STACK
