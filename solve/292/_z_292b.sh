#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== vuln : offset du buffer ==="
objdump -d -Mintel 292_vuln 2>/dev/null | sed -n '/<vuln>:/,/^$/p' | head -20
echo "=== .bss / writable ==="
readelf -S 292_vuln 2>/dev/null | grep -E "\.bss|\.data" | head -5
echo "=== segments ==="
readelf -l 292_vuln 2>/dev/null | grep -E "LOAD" | head -6
