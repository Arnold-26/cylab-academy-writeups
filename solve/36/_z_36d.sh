#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
objdump -d -Mintel 36_no_auth_mistery 2>/dev/null | sed -n '/<encode>:/,/^$/p' | head -60
echo "=== save / getValue ==="
objdump -d -Mintel 36_no_auth_mistery 2>/dev/null | grep -E "^0[0-9a-f]+ <" | head -12
