#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 184_fun
file 184_fun | cut -c1-110
echo "=== main ==="
objdump -d -Mintel 184_fun 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -45
echo "=== chaines ==="
strings -n 5 184_fun | head -12
