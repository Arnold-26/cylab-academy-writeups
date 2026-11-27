#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== formats / chaines proches ==="
strings -t x -n 3 181_vuln | grep -iE "^.*(%[0-9]*s|%[0-9]*d|fizz|buzz|flag|enter|number|correct|wrong)" | head -15
echo "=== suite de main ==="
objdump -d -Mintel --start-address=0x8049300 --stop-address=0x8049440 181_vuln 2>/dev/null | grep -E "call|lea +eax,\[ebp|mov +BYTE|push +0x" | head -30
