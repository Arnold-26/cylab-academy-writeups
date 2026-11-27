#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 75_zero_to_hero
file 75_zero_to_hero | cut -c1-110
readelf -h 75_zero_to_hero | grep Type
echo "=== symboles ==="
nm 75_zero_to_hero 2>/dev/null | grep -E " [Tt] " | head -15
echo "=== main ==="
objdump -d -Mintel 75_zero_to_hero 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -40
echo "=== fonctions interessantes ==="
objdump -d -Mintel 75_zero_to_hero 2>/dev/null | grep -E "^0[0-9a-f]+ <" | head -20
echo "=== chaines ==="
strings -n 5 75_zero_to_hero | head -15
