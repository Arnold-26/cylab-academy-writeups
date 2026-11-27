#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 306_vuln
file 306_vuln | cut -c1-110
echo "=== symboles ==="
nm 306_vuln 2>/dev/null | grep -E " (win|vuln|UnderConstruction|main)$"
echo "=== vuln : prologue et gets ==="
objdump -d -Mintel 306_vuln 2>/dev/null | sed -n '/<vuln>:/,/^$/p' | head -30
echo "=== win : buffer ==="
objdump -d -Mintel 306_vuln 2>/dev/null | sed -n '/<win>:/,/^$/p' | grep -E "sub esp|lea|fgets|mov" | head -12
