#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 435_chall
echo "=== type / protections ==="
file 435_chall | cut -c1-110
readelf -h 435_chall | grep Type
readelf -d 435_chall 2>/dev/null | grep -E "BIND_NOW" || echo "(pas de BIND_NOW)"
echo "=== symboles ==="
nm 435_chall 2>/dev/null | grep -E " (win|check_win|main)$"
objdump -d -Mintel 435_chall 2>/dev/null | sed -n '/<check_win>:/,/^$/p' | head -12
