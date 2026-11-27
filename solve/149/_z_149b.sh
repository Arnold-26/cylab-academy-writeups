#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
ls -la 149_checkpass 2>/dev/null
file 149_checkpass | cut -c1-110
echo "=== strings interessantes ==="
strings -n 5 149_checkpass | grep -aviE "glibc|gcc|\.so|\.c$|gnu|U$" | head -25
echo "=== execution ==="
printf 'test\n' | timeout 5 ./149_checkpass 2>&1 | head -6
