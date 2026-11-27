#!/bin/bash
cd /tmp/cylab_eps || exit 1
echo "=== relocations GOT ==="
readelf -rW 75_zero_to_hero 2>/dev/null | head -25
echo "=== adresse 0x601fe8 ==="
readelf -x .got.plt 75_zero_to_hero 2>/dev/null | head -8
echo "=== fonction option 1 (0x400a4d) complete ==="
objdump -d -Mintel --start-address=0x400a4d --stop-address=0x400bb3 75_zero_to_hero 2>/dev/null | grep -vE "^$" | head -60
