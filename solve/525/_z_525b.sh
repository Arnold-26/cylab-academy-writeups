#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 525_vuln
echo "=== protections ==="
file 525_vuln | cut -c1-120
readelf -h 525_vuln | grep Type
readelf -d 525_vuln 2>/dev/null | grep -E "BIND_NOW|FLAGS" | head -3
readelf -s 525_vuln 2>/dev/null | grep -c stack_chk
echo "=== fun ==="
objdump -d -Mintel 525_vuln 2>/dev/null | sed -n '/<fun>:/,/^$/p' | head -40
