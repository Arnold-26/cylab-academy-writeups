#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 36_no_auth_mistery 2>/dev/null
file 36_no_auth_mistery | cut -c1-110
echo "=== main ==="
objdump -d -Mintel 36_no_auth_mistery 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -70
