#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 122_brute
file 122_brute | cut -c1-110
echo "=== execution avec une entree ==="
printf 'test\n' | ./122_brute 2>&1 | head -5
echo "=== chaines ==="
strings -n 4 122_brute | grep -aiE "flag|correct|wrong|input|password|enter" | head -10
echo "=== main ==="
objdump -d -Mintel 122_brute 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -40
