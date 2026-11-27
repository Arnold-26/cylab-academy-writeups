#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/pm_215 || exit 1
chmod +x chall
file chall | cut -c1-120
echo "=== checksec-like ==="
readelf -h chall 2>/dev/null | grep -E "Type|Machine"
readelf -l chall 2>/dev/null | grep -E "GNU_STACK|GNU_RELRO"
echo "=== imports ==="
objdump -R chall 2>/dev/null | head -15
echo "=== chaines ==="
strings -n 6 chall | grep -aiE "calculating|found|flag|error" | head -5
echo "=== main ==="
objdump -d -Mintel chall 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -45
