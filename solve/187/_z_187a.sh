#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 187_vuln
echo "=== type ==="
file 187_vuln | cut -c1-120
readelf -h 187_vuln | grep Type
echo "=== symboles ==="
nm 187_vuln 2>/dev/null | grep -E " (hahaexploitgobrrr|main|doProcess)$"
echo "=== caracteristiques ==="
readelf -s 187_vuln 2>/dev/null | grep -c stack_chk
echo "=== main : boucle ==="
objdump -d -Mintel 187_vuln 2>/dev/null | sed -n '/<main>:/,/^$/p' | grep -E "call|mov|test" | head -12
