#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
chmod +x 126_gauntlet
file 126_gauntlet | cut -c1-110
echo "=== symboles ==="
nm 126_gauntlet 2>/dev/null | grep -E " [Tt] " | head -20
echo "=== main / vuln ==="
objdump -d -Mintel 126_gauntlet 2>/dev/null | sed -n '/<main>:/,/^$/p' | head -25
echo "=== win ==="
objdump -d -Mintel 126_gauntlet 2>/dev/null | sed -n '/<win>:/,/^$/p' | head -30
