#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 214_horse
echo "=== strings ==="
strings -n 5 214_horse | grep -aviE "glibc|gcc|\.so|gnu" | head -22
echo "=== fonctions ==="
objdump -d -Mintel 214_horse 2>/dev/null | grep -E "^[0-9a-f]+ <" | head -20
echo "=== execution avec entree ==="
printf 'hello\n' | timeout 5 ./214_horse 2>&1 | head -8
