#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/y483 || exit 1
echo "=== ASCII (n>=5) : 40 premieres ==="
strings -n 5 un.exe | head -40
echo "=== UTF-16 (l) ==="
strings -el -n 5 un.exe | head -30
echo "=== imports ==="
objdump -x un.exe 2>/dev/null | sed -n '/DLL Name/,$p' | head -30
