#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== packed ? ==="
upx -l 149_checkpass 2>&1 | head -5
readelf -SW 149_checkpass 2>/dev/null | awk '{print $2, $6, $7}' | head -22
echo "=== essais ==="
for p in test password academy "" ; do
  echo "--- '$p' ---"
  timeout 5 ./149_checkpass "$p" 2>&1 | head -3
done
