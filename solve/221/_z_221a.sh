#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== symbols ==="
nm 221_matrix 2>/dev/null | head -20
echo "=== strings autour de flag ==="
strings -n 4 221_matrix | grep -n -A3 -B3 -i 'flag' | head -20
echo "=== main ==="
objdump -d -Mintel 221_matrix 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -50
