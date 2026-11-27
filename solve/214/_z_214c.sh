#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== _start -> main ==="
objdump -d -Mintel 214_horse 2>/dev/null | sed -n '/<_start>:/,/^$/p' | grep -E "lea|call" | head -4
echo "=== search de asprintf / read / write dans le code ==="
objdump -d -Mintel 214_horse 2>/dev/null | grep -B6 "call.*<asprintf@plt>" | head -20
