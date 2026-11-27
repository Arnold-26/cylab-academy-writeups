#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 55_sice_cream
file 55_sice_cream | cut -c1-120
readelf -h 55_sice_cream | grep Type
readelf -lW 55_sice_cream 2>/dev/null | grep -E "GNU_STACK|GNU_RELRO"
echo "=== symboles ==="
nm 55_sice_cream 2>/dev/null | grep -E " [Tt] " | head -15
echo "=== main / vuln ==="
objdump -d -Mintel 55_sice_cream 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -40
echo "=== imports ==="
objdump -T 55_sice_cream 2>/dev/null | grep UND | awk '{print $NF}' | tr '\n' ' '
