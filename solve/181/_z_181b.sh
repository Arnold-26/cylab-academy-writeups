#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 181_vuln
file 181_vuln | cut -c1-120
echo "=== symboles ==="
nm 181_vuln 2>/dev/null | grep -E " [Tt] " | grep -viE "^0.* (__|_IO|_dl)" | head -20
echo "=== appels dangereux ==="
objdump -d -Mintel 181_vuln 2>/dev/null | grep -E "call.*(gets|read|scanf|fgets)@plt" | head -10
echo "=== chaines ==="
strings -n 6 181_vuln | grep -aiE "flag|fizz|buzz|win|oops|congrat" | head -12
