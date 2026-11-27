#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 215_chall
file 215_chall | cut -c1-110
readelf -h 215_chall | grep Type
echo "=== imports ==="
objdump -T 215_chall 2>/dev/null | grep -E "UND" | awk '{print $NF}' | head -20
echo "=== NX / stack ==="
readelf -lW 215_chall 2>/dev/null | grep -E "GNU_STACK|GNU_RELRO"
echo "=== gadgets utiles ==="
objdump -d -Mintel 215_chall 2>/dev/null | grep -E "pop +rdi|pop +rsi|pop +rdx" | head -6
echo "=== main ==="
objdump -d -Mintel 215_chall 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "call|lea|sub +rsp" | head -20
