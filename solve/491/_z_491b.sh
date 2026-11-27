#!/bin/bash
cd /tmp/cylab_eps || exit 1
chmod +x 491_vuln
echo "=== file ==="
file 491_vuln | cut -c1-100
echo "=== symboles ==="
nm 491_vuln 2>/dev/null | grep -E ' (win|main|call_functions)$'
readelf -s 491_vuln 2>/dev/null | grep -E ' win$| call_functions$' | head -4
echo "=== protections ==="
readelf -h 491_vuln | grep Type
readelf -s 491_vuln 2>/dev/null | grep -c stack_chk
