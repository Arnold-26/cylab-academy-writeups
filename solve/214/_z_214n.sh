#!/bin/bash
cd /mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps || exit 1
echo "=== gadgets verifies ==="
for a in 0x400c03 0x400c01 0x400828 0x400b96 0x400750; do
  echo "--- $a ---"
  objdump -d -Mintel --start-address=$a --stop-address=$((a+12)) 214_horse 2>/dev/null | tail -4
done
