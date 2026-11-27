#!/bin/bash
D="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_git/707"
cd "$D" || exit 1
mmls disk.img 2>/dev/null
echo "=== essai offsets ==="
for off in 2048 616448 1048576; do
  echo "--- offset $off ---"
  fls -o $off disk.img 2>/dev/null | head -8
done
