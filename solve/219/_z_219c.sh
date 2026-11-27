#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== .text complet (fin) ==="
objdump -d 219_riscy 2>/dev/null | sed -n '/100d2:/,$p' | head -60
echo "=== section headers ==="
readelf -S 219_riscy 2>/dev/null | grep -E 'rodata|text|data'
echo "=== rodata hex ==="
objdump -s -j .rodata 219_riscy 2>/dev/null | head -20
