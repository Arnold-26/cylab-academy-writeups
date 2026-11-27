#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/pm_213 || exit 1
chmod +x chall
readelf -h chall | grep -E "Type"
echo "=== symboles flag ==="
nm chall 2>/dev/null | grep -iE " flag|load_flag|main|HEADER" | head -10
echo "=== via readelf ==="
readelf -s chall 2>/dev/null | grep -i flag | head -5
echo "=== strings ==="
strings -n 5 chall | grep -aiE "welcome|flag" | head -3
