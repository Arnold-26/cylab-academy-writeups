#!/bin/bash
cd /tmp/cylab_eps || exit 1
objdump -d -Mintel 151_remote 2>/dev/null | grep -n -B3 -A12 "call.*MD5_Final" | head -40
echo "=== donnees .rodata ==="
readelf -x .rodata 151_remote 2>/dev/null | head -12
