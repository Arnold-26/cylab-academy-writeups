#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== fonctions ==="
objdump -d -Mintel 39_need-for-speed 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -20
echo "=== main (appels) ==="
objdump -d -Mintel 39_need-for-speed 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "call|mov +edi|lea" | head -30
