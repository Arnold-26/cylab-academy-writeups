#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 260_vuln
echo "=== type ==="
file 260_vuln | cut -c1-110
readelf -h 260_vuln | grep Type
echo "=== symboles ==="
nm 260_vuln 2>/dev/null | grep -E " (win|vuln|main)$"
echo "=== vuln : disposition ==="
objdump -d -Mintel 260_vuln 2>/dev/null | sed -n '/<vuln>:/,/^$/p' | grep -E "lea|mov|call|sub" | head -30
