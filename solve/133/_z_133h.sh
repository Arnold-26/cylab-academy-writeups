#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== gadgets ==="
objdump -d -Mintel 133_gauntlet 2>/dev/null | grep -E "pop +rdi" -A1 | head -8
echo "=== ret simple ==="
objdump -d -Mintel 133_gauntlet 2>/dev/null | grep -E "^ +400...:.*c3 +ret" | head -4
echo "=== offsets libc ==="
nm -D 133_libc-2.27.so 2>/dev/null | grep -E " (system|__libc_start_main)@@"
strings -a -t x 133_libc-2.27.so | grep -m1 "/bin/sh"
echo "=== imports du binaire ==="
objdump -T 133_gauntlet 2>/dev/null | grep "UND" | awk '{print $NF}' | tr '\n' ' '
