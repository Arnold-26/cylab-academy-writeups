#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== file/mitigations ==="
file 217_homework | cut -c1-120
readelf -l 217_homework 2>/dev/null | grep -E 'GNU_RELRO|GNU_STACK'
readelf -d 217_homework 2>/dev/null | grep -E 'BIND_NOW'
echo "=== symbols ==="
nm 217_homework 2>/dev/null | head -25
echo "=== strings ==="
strings -n 4 217_homework | grep -vE '^(GCC|GLIBC|__|_|\.)' | head -30
echo "=== fonctions ==="
objdump -d -Mintel 217_homework 2>/dev/null | grep -E '^[0-9a-f]+ <' | head -25
